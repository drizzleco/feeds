# Welcome to the Feeds API Documentation!

# Authorization

1. All requests must be authenticated with a token
2. Tokens can be created in the [Devices](/devices) page
3. Tokens, Dashboards, Feeds, and User Routes must be authenticated with a token that has User Scope
4. Data Routes must be authenticated with a token that has access to the Feed that the operation is intended for

To authenticate requests you may either:

1.  Provide `token` in the query string

    Ex:

    ```
    /api/dashboards?token=TOKEN_HERE
    ```

    **OR**

2.  Provide `token` in the JSON body

    Ex:

    ```
    {
        ...
        "token"="TOKEN_HERE"
    }
    ```

**NOTE:** To play around with the API below, make sure you're logged in or use the 'Authorize' button below to use a Token for authentication.
