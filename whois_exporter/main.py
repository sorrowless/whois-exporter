from datetime import datetime
from fastapi import FastAPI, Response
from textwrap import dedent

import whois

app = FastAPI()

@app.get("/")
async def root():
    data = '''
    <html>
    <head><title>Whois Exporter</title></head>
    <body>
            <h1>Whois Exporter</h1>
            <p><a href="/probe?target=google.com">probe google.com</a></p>
    </body>
    </html>
    '''
    return Response(content=data)

@app.get("/probe")
async def probe(
        target: str,
        force: bool = False,
        whois_server: str = None,
        verbose: bool = False):
    params = {
        "domain": target,
        "force": force,
        "server": whois_server,
        "verbose": verbose,
        "cache_age": 60*60*24
    }
    domain = whois.query(**{k:v for k,v in params.items() if v is not None})
    probeSuccess = 1 if domain else 0
    expiryDays = (domain.expiration_date - datetime.utcnow()).days if domain else -1
    domainResponseInfo = dedent(f"""
        # HELP domain_expiry_days time in days until the domain expires
        # TYPE domain_expiry_days gauge
        domain_expiry_days{{domain="{target}"}} {expiryDays}
        # HELP domain_probe_success wether the probe was successful or not
        # TYPE domain_probe_success gauge
        domain_probe_success{{domain="{target}"}} {probeSuccess}
    """)
    return Response(content=domainResponseInfo)