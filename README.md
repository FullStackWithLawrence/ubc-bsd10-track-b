# ubc-bsd10-track-b

Supplemental materials for UBC BSD10 Track B

## module 6 labs

I. Understanding LLM out-of-the-box capabilities
   Prompt: "Is Lawrence McDaniel a good photographer?" (15 minutes)

- Google
- ChatGPT
- Postman via OpenAI/GoogleAI/MetaAI
- curl via OpenAI
  - what's the difference?
  - streaming and other UX improvements
  - tool calling
  - ChatGPT's back door web search

II. Getting setup with api access (15 minutes)

- https://platform.openai.com/settings/organization/api-keys
- testing with curl
- setting up Postman
  - base url
  - required headers
  - body
  - handling sensitive data
  - trouble shooting

III. Getting setup with Python OpenAI PyPI (10 minutes)

- https://github.com/FullStackWithLawrence/openai-hello-world/
- clone
- make init
- make docker-build
- live demo
 
## module 7 labs

I. LLM Tool Call live example
   Prompt: "What's the weather in Vancouver right now?" (15 minutes)
    docs: https://platform.openai.com/docs/guides/function-calling?api-mode=responses
    example: https://platform.smarter.sh/docs/developer/weather-function/

- break down a tool call in smarter
  - ChatGPT
  - Postman
  - https://openai.lawrencemcdaniel.com/			-> https://github.com/FullStackWithLawrence/aws-openai
  - https://platform.smarter.sh/workbench/example/chat/

II. LLM RAG live example
    Prompt: "What analytics and accounting courses does Wharton offer?" (30 minutes)

- Google
  - ChatGPT
  - LLM Api prompt via Postman
  - RAG Prompt: https://github.com/FullStackWithLawrence/openai-embeddings

  - setup the project
  - build the vector database
  - demo template technique
  - demo with / without RAG approach
  - show a sample human language query to vector database
