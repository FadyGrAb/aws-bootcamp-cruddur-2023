# Week 0 — Billing and Architecture
## Required Homework:
Please note that I'v blurred out a part of my AWS account number and account name as this is public repo and I'm not comfortable with showing them in public.

### Recreate Conceptual Diagram in Lucid Charts or on a Napkin:
![napkin desing](assests/week00/Cruddur%20-%20Conceptual%20Diagram.png)
[Conceptual diagram share link](https://lucid.app/lucidchart/333b5391-85b9-4cdb-810f-c838492974d8/edit?view_items=eC5xYggEBhh_&invitationId=inv_b9a11869-c11b-4544-989e-b23d1867cbc1)

And on an actual napkin 😉. Sorry for the bad quality! It's very hard to write on a napkin 😅.
![actual napkin](assests/week00/napkin.jpg)

### Recreate Logical Architectual Diagram in Lucid Charts:
![Logical design](assests/week00/Crrudur%20-%20Logical%20diagram.png)
[Logical diagram share link](https://lucid.app/lucidchart/37994b73-3e91-4ee8-a765-7d16c5361ca3/edit?viewport_loc=-314%2C-29%2C2873%2C1342%2C0_0&invitationId=inv_f22e2ebf-5ef0-4aca-89d3-7fce914ff8f1)

### Generate AWS Credentials:
![access key 1](assests/week00/access%20key%201.png)
![access key 2](assests/week00/access%20key%202.png)

### Installed AWS CLI:
I am not confortable using my AWS credentials in other cloud services. So I'll use the AWS CLI from my local machine specially that I recall that you said in one of the videos that it will be used for administration. And this was one of the *recommendations* that appeared in the warning message when I tried to generate an Access key from IAM to use the CLI via IAM Identiy Center.  
![Access Keys recommendation](assests/week00/keyrecomendation.png)  
So I've installed it in my Windows local environement using powershell as follows:  
  
Searching for the package using `winget` to install the package from [Microsoft Package Manager service](https://learn.microsoft.com/en-us/windows/package-manager/winget/)
```pwsh
winget search aws             # To search for aws available packages.
```
!["aws cli package search"](assests/week00/awscli%201.png)
  
Installing the package
```pwsh
winget install amazon.awscli  # amazon.awscli is the package ID found in the results of the previous commands.
```
!["installing awscli"](assests/week00/awscli%202.png)
  
Using the CLI and logging in. I'm using IAM Identiy Center and logged in as the admin user using SSO (I use the sso only for CLI access)
![login](assests/week00/awscli%203.png)
  
### Create a Billing Alarm:
I've created a billing alarm using the console that will trigger at >10 USD.
![billing alarm](assets/../assests/week00/alarm.png)

### Create a Budget:
I've create only one budget in the console using the forecasted amount with a maximum of 10 USD which will trigger on 80%.
![budget](assests/week00/budget.png)

## Homework Challenges
### Locking down my root account:
![root user](assests/week00/hwc-root1.png)
  
As for the security recommendation, I don't have any affected policies
![affected policies](assests/week00/hwc-root2.png)

###  I've checked out the Well Architected Tool:
![Well architected](assests/week00/hwc-wellarchitected.png)
### Enabled IAM Identity Center and created an admin group and a user:
I've followed the official [IAM Identity Center user guide](https://docs.aws.amazon.com/singlesignon/latest/userguide/what-is.html) for this task and all of the following.  
  
The created user
![IAM Identity Center User](assests/week00/hwc-iamic-user.png)
The created Group
![IAM Identity Center Group](assests/week00/hwc-iamic-group.png)
### Forced IAM Identity Center users to use MFA:
And restrict their sessions to one hour.
![MFA](assests/week00/hwc-iamic-mfa.png)
### Created an IAM Identity Center permission set:
The permission set has only one policy to give full access to the AWS account and the sso session will be only one hour. I attached this permission set to the **Admins** group.
![permission set](assests/week00/hwc-iamic-permissionset.png)
### Using the AWS CLI with the IAM Identity Center Admin user:
![CLI](assests/week00/awscli%203.png)