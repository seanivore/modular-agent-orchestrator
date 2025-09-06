
## 1. User Login and UserID

### Core Objectives 

  1. Secure login via passkey or traditional using unique id of email or phone 
  2. System locates UserID or creates one with User's directory  
  3. UserID provides anonymous data, connects all User data 

### Secure Login Setup's UX and UI 

  - Inspired by domain website PORK-BUN's login flow 
    - Implementation plan in list above 
    - Illustrating the UX and how UI is laid out 

* **BUTTON (pressed): Log in to an Existing Account** 

  - This is the first page you are routed to 
    - FIELD: *Enter your email or phone* user identification 
    - FIELD: Standard *password* 
      - TEXT: Under password it says *"Leave password blank if using a passkey"* 
      - ACTUAL UX: Low risk precaution; you can enter anything and it *still works,* system just ignores it *creating flawless UX* 
      - Better UI than writing nothing or writing "You don't need to enter this if..." so it is sort of necessary even if it isn't adhered to 
  - BUTTON (automatic): Cloudflare auto-secure anti-spam *requires no action by the user* 
  - CHECK-MARK (pre-clicked): to *Remember Me* 

  - Pork-bun does *not make it clear that clicking LOGIN will bring up the passkey* and we might want to, though in retrospect it is obvious 

  - *Legal jargon:* By continuing you agree to the following: I acknowledge that I have read and agree to all Product Terms of Service, the Marketplace Agreement, and the Privacy Policy. You consent to enroll new automatic monthly subscription renewal service, which can be cancelled at any time via the Personal Preferences Billing section of your account. Automatic renewals are billed to payment method(s) specified on your Account Settings page until cancelled. If paying by credit card, you authorize {{ENTITY}} to send instructions to the financial institution that issued your card to take payments from your card account in accordance with the terms of your agreement with us. 

  - BUTTON: *Create New Account* is above the form, and also directly below the login button 
  - LINK: *Forgotten password, 2FA, or security key* below the login and second create new account button 

* **BUTTON (pressed): Create New Account**

  - This is a separate page navigated to from the initial login page unless sent directly from a link
    - BUTTON (automatic; no clicking needed): *Cloudflare* auto-secure anti-spam
  - FIELD: *EMAIL*  
  - FIELD: *PHONE* 
    - NOTE: One valid contact identification required as Account ID 
    - NOTE: You will be messaged to validate once during setup 
  - FIELD: *PASSWORD* 
    - NOTE: Must be 12 to 72 characters long, differ from your account ID, etc. 
  - CHECK-MARK: that they've read the legal jargon, terms of service, privacy policy 

  - BUTTON: *USE PASSKEY* 
    - This is directly below the password field 
    - Setting it up should automatically collect all information we need 
    - Best UX we should feature prominently 

  - *NOT REQUIRED* form fields 
    - Company Name, standard "will you be using this for personal, business, etc." 
    - Standard "what do you plan on delegating to automate with AI agents"  
    - We should brainstorm these questions so that we can be sure to NOT include many, but are including the best 

  - PAYMENT FORM: Next pay, for subscription 
    - Maybe consider free trial; see different configs and UI 
    - Use Stripe for UX and design of payment pages 

  - BUTTON: another pressed create account button at the bottom 
  - BUTTON: not pressed, right next to create account, *LOGIN TO EXISTING ACCOUNT* 

  - NOTE REGARDING MULTILINGUAL WEBSITE: "The word “passkey” *does not translate cleanly in every language*. Pair it with a short explanatory subtitle such as “Faster, one-tap sign-in with your device" advice given to me by AI when asking about pushing Passkey usage for our multilingual launch. Let this stand as a note reminder that we must check these kind of things, rather than just simply translating pages. It sounds like there might also be some issue with certain countries; this makes me think that we *likely will want to exclude our services to certain countries* as well. 

### System Locates or Creates UserID with User Directory 

* **UserID is created at first login**

  - It uses their *ACCOUNT ID* from the login information 
  - The `meid` script is used 
    - Provides the same UserID every time you enter the same Account ID 
    - Will always be formatted as `user-####` 
  - This example runs the `meid` as a script in the terminal for illustration 
  - As you can see, various phone number formats work, as well as the entirety of my email address 
    - the Account ID must always be *one single string of characters* 
    - *Our form fields should be strict in forcing specific formatting* known to work 

```bash 
  > meid horvathaugust@gmail.com                     # Used entire email address
  Username 'horvathaugust@gmail.com' -> user-5253    # Response 
```

```bash
  > meid 424-744-7687
  Username '424-744-7687' -> user-0697      # Hyphenated phone number
  > meid 4247447687
  > meid 424.744.7687
  Username '4247447687' -> user-0697        # No hyphens or periods has same result 
```

* **User directory setup automatically during New User Setup** 

  - User `./configs/user/` directory, *as structured below*
    - Includes other essential user data files 
    - Core for logging preferences and more 
    - Analytics files are created and updated as user interacts with the app 

  - *NOTE: REQUIRED FUNCTIONALITY UPDATE*
    - We built everything using a 'username' 
    - Will will instead use an Account ID that is unique by design 
    - The *file name* and *directory names* must be UserID; they currently create directories using the defunct "username" 

```
configs/user/...
└── user-5253      # Since we have multiple unique identifiers, the directory must be named with the UserID 
    ├── analytics                       # All need to be reviewed and labeled
    │   ├── cost_tracking.json 
    │   ├── session_metrics.json
    │   ├── tool_usage.json
    │   └── workflow_metrics.json
    ├── memories                        # Review, label, detail management details in codebase, updates 
    │   ├── personal_preferences.json
    │   └── project_context.json
    └── user_seanivore.json             # Delta-only storage of User application preferences *ANOTHER THAT HAS DEFUNCT USERNAME LOGIC*
``` 

* **User login that has logged in before** 

  - System dynamically searches the `./configs/user/` directory for their *Account ID*
    - When found, it pulls up their *UserID* needed for all in-app identification 

* **The first user analytics are triggered at this point** 

  - *Details to come* when we review this flow and match up operations with files 
    - Let's *detail each trigger* and when it goes off 
    - This will make it easier to visualize and thus build out more 
