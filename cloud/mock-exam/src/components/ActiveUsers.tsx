import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";

export function ActiveUsers() {
  const [activeUsers, setActiveUsers] = useState<number>(0);
  const [isConfigured, setIsConfigured] = useState<boolean>(true);

  useEffect(() => {
    // Basic check if the user hasn't configured the environment variables yet
    const url = import.meta.env.VITE_SUPABASE_URL || "YOUR_SUPABASE_URL_HERE";
    if (url === "YOUR_SUPABASE_URL_HERE" || !url.startsWith("http")) {
      setIsConfigured(false);
      return;
    }

    // Create a random user ID for this session
    const userId = crypto.randomUUID();

    // Create a presence channel
    const roomOne = supabase.channel("online-users", {
      config: {
        presence: {
          key: userId,
        },
      },
    });

    roomOne
      .on("presence", { event: "sync" }, () => {
        const state = roomOne.presenceState();
        // Count all unique users
        const count = Object.keys(state).length;
        setActiveUsers(count);
      })
      .subscribe(async (status) => {
        if (status === "SUBSCRIBED") {
          // Track this user
          await roomOne.track({
            online_at: new Date().toISOString(),
          });
        }
      });

    return () => {
      // Cleanup when component unmounts
      supabase.removeChannel(roomOne);
    };
  }, []);

  if (!isConfigured) {
    return (
      <div className="fixed top-4 right-4 z-50 flex items-center gap-2 border border-destructive bg-black px-3 py-1.5 text-xs text-destructive font-mono">
        <span className="animate-pulse">●</span>
        <span>SUPABASE NOT CONFIGURED</span>
      </div>
    );
  }

  return (
    <div className="fixed top-4 right-4 z-50 flex items-center gap-2 border border-primary bg-black px-3 py-1.5 text-xs text-primary font-mono shadow-[0_0_10px_rgba(34,197,94,0.2)]">
      <span className="animate-pulse text-green-500">●</span>
      <span>{activeUsers} USER{activeUsers !== 1 ? "S" : ""} ONLINE</span>
    </div>
  );
}
