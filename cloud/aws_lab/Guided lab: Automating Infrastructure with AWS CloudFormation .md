Guided Lab: Automating Infrastructure Deployment with AWS CloudFormation

 
Lab overview and objectives

Deploying infrastructure in a consistent, reliable manner is difficult. It requires people to follow documented procedures without taking any undocumented shortcuts. It can also be difficult to deploy infrastructure after hours when fewer staff are available. AWS CloudFormation changes this situation by defining infrastructure in a template that can be automatically deployed—even on an automated schedule.

In this lab, you learn how to deploy multiple layers of infrastructure with AWS CloudFormation, update a CloudFormation stack, and delete a stack (while retaining some resources).

After completing this lab, you should be able to do the following:

    Use AWS CloudFormation to deploy a virtual private cloud (VPC) networking layer.

    Use AWS CloudFormation to deploy an application layer that references the networking layer.

    Explore templates with AWS Infrastructure Composer.

    Delete a stack that has a deletion policy.


Duration

This lab will require approximately 20 minutes to complete.

AWS service restrictions

In this lab environment, access to AWS services and service actions might be restricted to the ones that are needed to complete the lab instructions. You might encounter errors if you attempt to access other services or perform actions beyond the ones that are described in this lab.

Accessing the AWS Management Console

    At the top of these instructions, choose  Start Lab.

        The lab session starts.

        A timer displays at the top of the page and shows the time remaining in the session.

         Tip: To refresh the session length at any time, choose  Start Lab again before the timer reaches 0:00.

        Before you continue, wait until the circle icon to the right of the AWS  link in the upper-left corner turns green. When the lab environment is ready, the AWS Details panel will also display.

    To connect to the AWS Management Console, choose the AWS link in the upper-left corner above the terminal window.

        A new browser tab opens and connects you to the console.

         Tip: If a new browser tab does not open, a banner or icon is usually at the top of your browser with a message indicating that your browser is preventing the site from opening pop-up windows. Choose the banner or icon, and then choose Allow pop-ups.

    Arrange the AWS Management Console tab so that it displays alongside these instructions. Ideally, you will have both browser tabs open at the same time so that you can follow the lab steps more easily.

     Do not change the Region unless specifically instructed to do so.


Task 1: Deploying a networking layer

It's a best practice to deploy infrastructure in layers. Common layers include the following:

    Network (Amazon Virtual Private Cloud)

    Database

    Application

This way, templates can be reused between systems. For example, you can deploy a common network topology between development, test, and production environments, or deploy a standard database for multiple applications.

In this task, you deploy an AWS CloudFormation template that creates a networking layer by using Amazon VPC.

    Open the context (right-click) menu for the following link and download the template to your computer: lab-network.yaml

     If you want, you can open the template in a text editor to see how the AWS resources are defined.

    Templates can be written in JSON or YAML. YAML is a markup language that is similar to JSON, but it is more convenient to read and edit.

    At the top of the AWS Management Console, in the search box, search for and choose CloudFormation.

    Choose Create stack > With new resources (standard) and configure these settings:

    Step 1: Create stack

        Prepare template: Choose  Template is ready.

        Template source: Choose Upload a template file > Choose file, and then choose the lab-network.yaml file that you downloaded.

        Choose Next.

    Step 2: Specify stack details

        Stack name: lab-network

        Choose Next.

    Step 3: Configure stack options

        In the Tags section, choose Add new tag and configure the following:

            Key: application

            Value: inventory

        Choose Next.

    Step 4: Review and create

        Choose Submit.

    The template is used by AWS CloudFormation to generate a stack of resources in the AWS account.

    The specified tags are automatically propagated to the resources that are created, which helps identify resources that are used by particular applications.

    Choose the Stack info tab.

    Wait for the Status to change to CREATE_COMPLETE.

     Choose Refresh  every 15 seconds to update the display, if necessary.

    You can now examine the resources that were created.

    Choose the Resources tab.

    You see a list of the resources that were created by the template.

     If the list is empty, update the list by choosing Refresh .

    Choose the Events tab and browse through the events.

    The events show (from most recent to least recent) the activities that were performed by AWS CloudFormation. Example events include starting to create a resource and then completing the resource creation. Any errors that were encountered during the creation of the stack is listed in this tab.

    Choose the Outputs tab.

    A CloudFormation stack can provide output information, such as the IDs of specific resources and links to resources.

    The following two outputs are listed:

        PublicSubnet:  The ID of the public subnet that was created (for example: _subnet-08aafd57f745035f1__)

        VPC: The ID of the virtual private cloud (VPC) that was created (for example: vpc-08e2b7d1272ee9fb4) 

        Outputs can also be used to provide values to other stacks. This is shown in the Export name column. In this case, the VPC and subnet IDs are given export names so that other stacks can retrieve the values. These other stacks can then build resources inside the VPC and subnet that were just created. You use these values in the next task.

    Choose the Template tab.

    This tab shows the template that was used to create the stack—that is, the template that you uploaded while you created the stack. Don't hesitate to examine the template and see the resources that were created or explore the Outputs section at the end (this section defined which values to export).


Task 2: Deploying an application layer

Now that you deployed the network layer, you will deploy an application layer that contains an Amazon Elastic Compute Cloud (Amazon EC2) instance and a security group.

The AWS CloudFormation template imports the VPC and subnet IDs from the outputs of the existing CloudFormation stack. Then, it uses this information to create the security group in the VPC and the EC2 instance in the subnet.

    Open the context (right-click) menu for the following link and download the template to your computer: lab-application.yaml

     If you want, you can open the template in a text editor to see how resources are defined.

    From the top, choose Create stack > With new resources (standard), and then configure these settings:

Step 1: Create Stack

    Prepare template: Choose  Template is ready.

    Template source: Choose Upload a template file > Choose file, and then choose the lab-application.yaml file that you downloaded.

    Choose Next.

Step 2: Specify stack details

    Stack name: lab-application

    Notice the NetworkStackName: lab-network

    Choose Next.

     The Network Stack Name parameter tells the template the name of the first stack that you created (lab-network), so it can retrieve values from the outputs.

Step 3: Configure stack options

    In the Tags section, choose Add new tag and configure the following:

        Key: application

        Value: inventory

    Choose Next.

Step 4: Review and create

    Choose Submit.

While the stack is being created, examine the details in the Events tab and the Resources tab. You can monitor the progress of the resource-creation process and the resource status.

    In the Stack info tab, wait for the Status to change to CREATE_COMPLETE.

    Your application is now ready!

    Choose the Outputs tab.

    Copy the URL that is displayed, open a new web browser tab, paste the URL, and press ENTER.

    The browser tab opens the application, which is running on the web server that this new CloudFormation stack created.

    A CloudFormation stack can use reference values from another CloudFormation stack. For example, this portion of the lab-application template references the lab-network template:

      WebServerSecurityGroup:

        Type: AWS::EC2::SecurityGroup

        Properties:

          GroupDescription: Enable HTTP ingress

          VpcId:

            Fn::ImportValue:

              !Sub ${NetworkStackName}-VPCID

The last line uses the network stack name that you provided (lab-network) when the stack was created. It imports the value of lab-network-VPCID from the outputs of the first stack. It then inserts the value into the VPC ID field of the security group definition. The result is that the security group is created in the VPC that was created by the first stack.

Here is another example, which is in the CloudFormation template that you just used to create the application stack. This template code places the EC2 instance into the subnet that was created by the network stack:

      SubnetId:

        Fn::ImportValue:

        !Sub ${NetworkStackName}-SubnetID

It takes the subnet ID from the lab-network stack and uses it in the lab-application stack to launch the instance into the public subnet, which was created by the first stack.

Task 3: Updating a Stack

AWS CloudFormation can also update a stack that was deployed. When you update a stack, AWS CloudFormation will only modify or replace the resources that are being changed. Any resources that are not being changed will be left as-is.

In this task, you update the lab-application stack to modify a setting in the security group.

First, you examine the current settings for the security group.

    At the top of the AWS Management Console, in the search box, search for and choose EC2.

    In the left navigation pane, in the Network & Security section, choose Security Groups.

    Select the check box for  lab-application-WebServerSecurityGroup.

    Choose the Inbound rules tab.

    Currently, only one rule is in the security group. The rule permits HTTP traffic.

    You now return to AWS CloudFormation to update the stack.

    From the Services menu at the top, choose CloudFormation.

    Open the context (right-click) menu for the following link and download the updated template to your computer: lab-application2.yaml

    This template has an additional configuration to permit inbound HTTPS traffic on port 443:

      - IpProtocol: tcp

        FromPort: 443

        ToPort: 443

        CidrIp: 0.0.0.0/0

    From the Stacks list of the AWS CloudFormation console, choose  lab-application.

    Choose Update and configure these settings:

    Prepare template: Choose  Replace current template.

    Template source: Choose  Upload a template file.

    Upload a template file:  Choose file, and then choose the lab-application2.yaml file that you downloaded.

    Choose Next on each of the next three screens to go to the Review lab-application page.

    In the Change set preview section at the bottom of the page, AWS CloudFormation displays the following resources that will be updated:

    Image shows Change set preview

    This change set preview indicates that AWS CloudFormation will modify the WebServerSecurityGroup without needing to replace it (Replacement = False). This change set means that the security group will have a minor change applied to it, and no references to the security group will need to change.

    Choose Submit.

    In the Stack info tab, wait for the Status to change to UPDATE_COMPLETE.

      Update the status by choosing Refresh  every 15 seconds, if necessary.

     You can now verify the change.

    Return to the Amazon EC2 console, and from the left navigation pane, choose Security Groups.

    In the Security Groups list, choose lab-application-WebServerSecurityGroup.

    The Inbound rules tab should display an additional rule that allows HTTPS traffic over TCP port 443.

    Note: This rule is added only to demonstrate the ability to update a stack using a CloudFormation template. Application is accessed on the port 80 only.

    This subtask demonstrates how changes can be deployed in a repeatable, documented process. The AWS CloudFormation templates can be stored in a source code repository (such as AWS CodeCommit). This way, you can maintain versions and a history of the templates and infrastructure that were deployed.


Task 4: Exploring templates with Infrastructure Composer

Infrastructure Composer is a graphic tool for creating, viewing, and modifying AWS CloudFormation templates. With Composer, you can diagram your template resources by using a drag-and-drop interface, and then edit their details through the integrated JSON and YAML editor.

Whether you are a new to AWS CloudFormation or an experienced AWS CloudFormation user, Composer can help you quickly see the interrelationship between a template's resources. It also enables you to easily modify templates.

In this task, you gain some hands-on experience with Composer.

    From the Services  menu, choose Cloudformation.

    In the left navigation pane, choose Infrastructure Composer.

    Tip: You might need to expand the left navigation pane by choosing the menu icon.

    In the Infrastructure Composer interface (within the main canvas area), choose the Menu button, select Open > Template file, and upload the lab-application2.yaml template that you downloaded previously.

    Infrastructure Composer displays a graphical representation of the template that's similar to the following:

   Image shows CloudFormation Infrastructure Composer interface with the AWS resources

Instead of drawing a typical architecture diagram, Infrastructure Composer is a visual editor for AWS CloudFormation templates. It draws the resources that are defined in a template and their relationship to each other.

    Experiment with the features of the Infrastructure Composer. Some things to try are the following:

    Select a resource on the Canvas. The Resource properties panel on the right side of the screen then displays the configurable properties for that specific resource. You can switch to the Template tab in the main view area to see how these changes are reflected in the YAML/JSON code.

    Try dragging a new resource from the Resource types pane on the left into the design area. The definition of the resource will be automatically inserted into the template code in the lower pane.

    Try dragging the resource connector circles to create relationships between resources (e.g., connecting an EC2 instance to a Security Group).

    Open the lab-network.yaml template that you downloaded earlier in the lab, and also explore its resources in Infrastructure Composer.


Task 5: Deleting the stack

When resources are no longer required, AWS CloudFormation can delete the resources built for the stack.

A deletion policy can also be specified against resources. It can preserve or (in some cases) back up a resource when its stack is deleted. This feature is useful for retaining databases, disk volumes, or any resource that might be needed after the stack is deleted. It can also be configured to retain important resources from getting deleted unintentionally.

The lab-application stack was configured to take a snapshot of an Amazon Elastic Block Store (Amazon EBS) disk volume before it's deleted. The code in the template that accomplishes that configuration is the following:

  DiskVolume:

    Type: AWS::EC2::Volume

    Properties:

      Size: 100

      AvailabilityZone: !GetAtt WebServerInstance.AvailabilityZone

      Tags:

        - Key: Name

          Value: Web Data

    DeletionPolicy: Snapshot

The DeletionPolicy in the final line directs AWS CloudFormation to create a snapshot of the disk volume before it's deleted.

You now delete the lab-application stack and see the results of this deletion policy.

    Return to the main AWS CloudFormation console by choosing Close at the top of the Composer page (choose Leave page if prompted).

    In the list of stacks, choose the lab-application link.

    Choose Delete.

    On the Delete stack? dialog box, choose Delete.

    You can monitor the deletion process in the Events tab and update the screen by choosing Refresh  occasionally. You might also see an events log entry that indicates that the EBS snapshot is being created.

    Wait for the stack to be deleted. It will disappear from the stacks list.

    The application stack was removed, but the network stack remained untouched. This scenario reinforces the idea that different teams (for example, the network team or the application team) can manage their own stacks.

    You will now verify that a snapshot of the EBS volume was created before the EBS volume was deleted.

    From the Services menu, choose EC2.

    In the left navigation pane, in the Elastic Block Store section, choose Snapshots.

    You see a snapshot Web Data with a Started time in the last few minutes, and it changes to Completed soon.

  
Submitting your work

    At the top of these instructions, choose Submit to record your progress and when prompted, choose Yes.

    If the results don't display after a couple of minutes, return to the top of these instructions and choose Grades.

    Tip: You can submit your work multiple times. After you change your work, choose Submit again. Your last submission is what will be recorded for this lab.

    To find detailed feedback on your work, choose Details followed by  View Submission Report.