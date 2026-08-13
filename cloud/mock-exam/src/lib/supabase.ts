import { createClient } from "@supabase/supabase-js";

// Use a valid dummy URL fallback so it doesn't crash the app if env vars are missing
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || "https://dummy.supabase.co";
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || "dummy-key";

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
