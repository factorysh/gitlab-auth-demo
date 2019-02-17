# Gitlab Auth Demo

Gitlab can provides JWT token, for delegating actions.

Docker Registry uses this token, and CI fetch sources with a token.

Tokens use asymetric RSA signature.

## Check certificate

    openssl x509 -text -noout -in public.pem

## Test it

Get the **public** certificate from your Gitlab instance.

Go get a _personnal access token_ `/profile/personal_access_tokens`.

Set environments variables.

```bash
export GITLAB=gitlab.example.com
export PROJECT=demo/myproject
export TOKEN=my_personal_access_token
export USER=jdoe
```

```bash
python3 -m venv
source ./venv/bin/activate
pip install -r requirements.txt
./demo.py
```

You can dump the certificate, with the python tool, installed in the `venv`

```bash
cat public.pem | x5092json | jq .
```

### Licence

3 terms BSD licences. © 2019 Mathieu Lecarme.
