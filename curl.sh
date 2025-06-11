


curl --location 'https://api.openai.com/v1/chat/completions' \
--header 'Authorization: Bearer sk-proj-<-- SECRET TOKEN -->' \
--header 'Content-Type: application/json' \
--header 'Cookie: __cf_bm=nJ1cxXL5o0HRj9BbxTeVj7grOd2uVnhIO13AcvA95mA-1749666130-1.0.1.1-WhClUxTpgjI7XrIMsXbG.2LgwuvTQAsiqirkpw1TSPD7oWGoPol6BEV7aTa4XuEDMGmwtr1RpSmGunl15wvfyMlH98cOUrGZ499u1BMabvw; _cfuvid=ylb4vn_iNmHY0FSzo3H2IoYPnQeJYbieeAP5EQu2Pyw-1749664430294-0.0.1.1-604800000' \
--data '{
    "model": "gpt-4o-mini",
    "messages": [
        {
            "role": "user",
            "content": "Is Lawrence McDaniel a good photographer?"
        }
    ]
}'