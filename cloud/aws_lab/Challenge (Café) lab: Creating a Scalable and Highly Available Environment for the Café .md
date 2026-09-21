Challenge Lab: Creating a Scalable and Highly Available Environment for the Café

 
Scenario

The café will soon be featured on a famous TV food show. When the show airs, Sofía and Nikhil anticipate that the café’s web server will experience a temporary spike in the number of users—perhaps even up to tens of thousands of users. Currently, the café’s web server is deployed in one Availability Zone, and Sofía and Nikhil are worried that the website won’t be able to handle the expected increase in traffic. They want to ensure that their customers have a great experience when they visit the website and that they don’t experience any issues, such as lags or delays in placing orders.

To ensure this experience, the website must be responsive, able to scale both up and down to meet fluctuating customer demand, and be highly available. Instead of overloading a single server, the architecture must distribute customer order requests across multiple application servers so it can handle the increase in demand.

In this lab, you take on the role of Sofía to implement a scalable and highly available architecture for the café's web application.
Lab overview and objectives

In this lab, you use Elastic Load Balancing (ELB) and Amazon EC2 Auto Scaling to create a scalable and highly available environment on Amazon Web Services (AWS).

After completing this lab, you should be able to do the following:

    Inspect a virtual private cloud (VPC).
    Update a network to work across multiple Availability Zones.
    Create an Application Load Balancer.
    Create a launch template.
    Create an Auto Scaling group.
    Set an alarm on a system metric to initiate auto scaling.
    Test load balancing and automatic scaling.

When you start the lab, your architecture will look like the following example:

 

Following diagram shows various infrastructure components available to learner when the lab starts.

At the end of this lab, your architecture should look like the following example:

 

Following diagram shows the architecture when the lab is finally built.

Note: In this challenge lab, step-by-step instructions are not provided for most tasks. You must figure out how to complete the tasks on your own.
Duration

This lab requires approximately 90 minutes to complete.
AWS service restrictions

In this lab environment, access to AWS services and service actions might be restricted to the ones that are needed to complete the lab instructions. You might encounter errors if you attempt to access other services or perform actions beyond the ones that are described in this lab.
Accessing the AWS Management Console

    At the top of these instructions, choose  Start Lab.

        The lab session starts.

        A timer displays at the top of the page and shows the time remaining in the session.

         Tip: To refresh the session length at any time, choose  Start Lab again before the timer reaches 0:00.

        Before you continue, wait until the circle icon to the right of the AWS  link in the upper-left corner turns green. When the lab environment is ready, the AWS Details panel displays.

    To connect to the AWS Management Console, choose the AWS link in the upper-left corner above the terminal window.

        A new browser tab opens and connects you to the console.

         Tip: If a new browser tab does not open, a banner or icon is usually at the top of your browser with a message that your browser is preventing the site from opening pop-up windows. Choose the banner or icon, and then choose Allow pop-ups.

    Arrange the AWS Management Console tab so that it displays alongside these instructions. Ideally, you have both browser tabs open at the same time so that you can follow the lab steps.

 
A business request for the café: Implementing a scalable and highly available environment (challenge)

Sofía understands that she must complete some tasks to implement high availability and scalability for the café’s web application. However, before changing the café’s application architecture, Sofía must evaluate its current state.

In the next several tasks, you work as Sofía to create and configure the resources that you need to implement a scalable and highly available application.
Task 1: Inspecting your environment

In this task, you evaluate your current lab environment.

    Explore the lab environment, including how the network is set up.

    Tip: You might want to start in the Amazon Virtual Private Cloud (Amazon VPC) console.

    To help you explore, continue to the next section and answer the questions about this lab.

Answering questions about the lab

Your answers are evaluated when you choose the blue Submit button at the end of the lab.

    To access the questions in this lab, at the top of these instructions, choose AWS Details.

    Choose the Access the multiple choice questions link.

    On the page that loads, answer each question, and choose Submit:
        Question 1: Which ports are open in the CafeSG security group?
        Question 2: Can you connect from the internet to instances in Public Subnet 1?
        Question 3: Should an instance in Private Subnet 1 be able to reach the internet?
        Question 4: Should an instance in Private Subnet 2 be able to reach the internet?
        Question 5: Can you connect to the CafeWebAppServer instance from the internet?
        Question 6: What is the name of the Amazon Machine Image (AMI)?

Task 2: Updating a network to work across multiple Availability Zones
Task 2.1: Creating a NAT gateway for the second Availability Zone

To achieve high availability, the architecture must span at least two Availability Zones. However, before you launch Amazon Elastic Compute Cloud (Amazon EC2) instances for your web application servers in the second Availability Zone, you must create a NAT gateway for them. A NAT gateway allows instances that do not have a public IP address to access the internet.

    Create a NAT gateway in the Public Subnet in the second Availability Zone.
    Configure the network to send internet-bound traffic from instances in Private Subnet 2 to the NAT gateway that you just created.

 
Task 3: Creating a launch template

During the lab setup, an AMI was created from the CafeWebAppServer instance. In this task, you create a launch template by using this AMI.  

    Create a launch template by using the AMI that was created during lab setup, and configure the following options:

    Launch template name: Enter a name for your launch template.

    Application and OS Images (Amazon Machine Image): From My AMIs, choose Cafe WebServer Image.
    Tip: To locate the AMI, choose the AMI dropdown menu, and enter Cafe.

    Instance type: Choose t2.micro.
    Tip: To locate the instance type, choose the Instance type dropdown menu, and enter t2.

    Key pair (login): Choose Create new key pair.
    Tip: Create a new key pair and choose it. Make sure that you download the key pair to your local computer.

    Security groups: Enter CafeSG.
    Tip: To locate the security group, in the Network settings section, choose the Security groups dropdown menu, and enter CafeSG.

    Resource tags: Choose Add new tag, and configure the following options:
        Key: Enter Name.
        Value: Enter webserver.
        Resource types: Choose Instances.

    IAM instance profile: Choose CafeRole.
    Tip: For this setting, expand the Advanced details section.

Task 4: Creating an Auto Scaling group

Now that the launch template is defined, you create an Auto Scaling group for the instances. In this task, do not create a load balancer when you create the Auto Scaling group. You create a load balancer in the next task. 

While creating an Auto Scaling group, you set a metric (CPU utilization) to initiate auto scaling events.

    To create a new Auto Scaling Group, configure the following options:

    Auto Scaling group name: Enter a name for your Auto Scaling group.

    Launch template: Choose the launch template that you created in the previous task.

    VPC: Use the VPC that was configured for this lab.

    Availability Zones and subnets: Choose Private Subnet 1 and Private Subnet 2.

    Advanced options: Skip these options.

    Group size:
        Desired capacity: Enter 2.
        Min desired capacity: Enter 2.
        Max desired capacity: Enter 6.

    Automatic scaling - optional: Choose Target tracking scaling policy, and configure the following options:
        Metric type: Choose Average CPU utilization.
        Target value: Enter 25.
        Instance warmup: Enter 60.

    To verify that you created the Auto Scaling group correctly, go to the Amazon EC2 console. You should have two instances, both with the name that you configured as Resource tags in the previous task.

Task 5: Creating a load balancer

Now that your web application server instances are deployed in private subnets, you need a way for the outside world to connect to them. In this task, you create a load balancer to distribute traffic across your private instances.

    To create an HTTP Application Load Balancer, configure the following options:

    Load balancer name: Enter a name for your load balancer.
    VPC: Use the VPC configured for this lab.
    Subnets: Use the two public subnets.
    HTTPS security configuration settings: Skip these settings.
    Security groups: Create a new security group that allows HTTP traffic from anywhere.
    Target group: Create a new target group.
    Registering targets: Skip this section.

Note: Wait until the load balancer is active before you move onto the next steps.

    Modify the Auto Scaling group that you created in the previous task by adding this new load balancer.

Hint: Add the target group that you created in the Application Load Balancer configuration.

Sofía has now created and configured the resources that the web application needs in order to be highly available and scalable. However, Sofía knows that she still has more work to do. To complete the process of updating the application architecture, Sofía must test the café’s web application to make sure that it performs as expected.

In the next tasks, you continue working in the role of Sofía and test whether the café web application automatically scales under load.
Task 6: Testing load balancing and automatic scaling
Task 6.1: Testing the web application without load

In this task, you test the café web application.

    To test the café web application, visit the DNS name of your load balancer and add /cafe to the end of the URL.

The café application should load.

If it does not, go back through the lab tasks and check your work. Pay attention to the following resources:

    Network configuration: Did you add the NAT gateway correctly?
    Route tables: Did you update the route tables with the NAT gateway?
    Launch template: Does the instance specify an IAM role?
    Load balancer: Is the load balancer in the public subnets?
    Instances: Are the instances deployed from the Auto Scaling group that is in the correct subnets?
    Security groups: Do the security groups allow HTTP traffic from the internet?

Task 6.2: Testing automatic scaling under load

In this task, you test whether the café application scales out automatically.

    By using AWS Systems Manager Session Manager, connect to one of the running web server instances.
    On the sessions manager terminal, use the following commands to start a stress test. This test increases the load on the web server CPU:

sudo amazon-linux-extras install epel

sudo yum install stress -y

stress --cpu 1 --timeout 600

    Verify that the Auto Scaling group deploys new instances.

    Continue to observe the Amazon EC2 console.
    During the test, you should observe that more web server instances are deployed.

Update from the café

After Sofía finishes testing the café web application's performance, she tells her parents about the change: when traffic increases, the café application now successfully scales out. Frank and Martha are impressed that Sofía implemented a highly available and scalable architecture for the application.

Meanwhile, the entire café team is excited. They are busy preparing for the increased volume of orders that they anticipate from being featured on the TV show. As they work on their preparations, they know that they can rely on automatic scaling to help them take orders and delight new customers.
Submitting your work

    At the top of these instructions, choose Submit to record your progress, and when prompted, choose Yes.
    If the results don't display after a couple of minutes, return to the top of these instructions and choose Grades.

 Tip: You can submit your work multiple times. After you change your work, choose Submit again. Your last submission is what will be recorded for this lab.

    To find detailed feedback on your work, choose Submission Report.