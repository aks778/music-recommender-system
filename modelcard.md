# Model Card for FindBeats

## Reflection

## What are the limitations or biases in your system?

There are only 18 songs in songs.csv so a lot of genres are not represented, which could be a problem if the user requests a genre that isn't accounted for in songs.csv. Additionally, if genre matches it scores +2 points, but mood scores +1 point for a match, which means genre overpowers mood, so in a case where the user cares more about mood than genre, the system will fail to deliver.

## Could your AI be misused, and how would you prevent that

I think the risk of it being misused is negligible because it's a music recommender system; however, if the extract_prefs method misunderstands user input, then recommendations which have nothing to do with what the user wanted will be provided.

## What surprised you while testing your AI's reliability?

I was surprised by how qwen2.5:0.5b was returning songs which didn't even exist in songs.csv confidently, which showed me that AI would come up with its own answers when it didn't know what to do. I changed the architecture of the system from tool-calling to prompt-inject RAG because of errors in findbeats.log, and so this showed me that the same AI model can behave in different ways depending on how it's used.

## Describe your collaboration with AI during this project. Identify one instance when the AI gave a helpful suggestion and one instance where its suggestion was flawed or incorrect.

I primarily used Claude Code for this project. It was very helpful in understanding the feature I wanted to implement and a helpful suggestion it gave me was to switch to prompt injection RAG instead of tool calling which led to the model giving correct answers. An instance where its suggestion was flawed was when it added a method to replace the placeholders when printing in order to fix model hallucination, but it ultimately resulted in tool calling not working properly, and so the method had to be removed.
