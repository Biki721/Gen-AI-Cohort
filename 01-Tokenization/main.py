import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
text = "Hello, I am Biki Dey"

tokens = enc.encode(text)
print("tokens : ",tokens)

decode = enc.decode(tokens)
print("Decoded tokens : ",decode)
