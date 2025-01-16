---
layout: post
title: Generating Software Architecture Diagrams with LLMs
description: Adventures in generating software architecture diagrams using Claude and ChatGPT
date: 2025-01-16 17:40:00
categories: LLM, architecture diagrams
---
**TL;DR: Claude is pretty good at generating simple software architecture diagrams but not so good at editing them. ChatGPT is bum**

I needed to create a simplified architecture diagram for an investor deck, so like any modern human I tried to avoid doing the work by delegating it to AI.

I started by feeding the following prompt into ChatGPT:
```none
Can you generate me a software platform architecture diagram in the style of an AWS diagram. This diagram will go in an investor deck so must look professional.

It should show:
- A react native mobile app
- The app should be calling an API which lives on AWS and connects to a postgres RDS database
- The API is making calls to the external APIs:
	- Anthropic
	- Strava
	- Garmin
	- Apple HealthKit
- The API also has a data science service which it calls which is also hosted on AWS
```

As you can see I am a very polite man when talking to people and machines. I'm sure the machines will remember who had polite prompts come judgment day.

The ChatGPT diagram whilst creative is comically bad.

![ChatGPT generated software architecture diagram](/assets/images/posts/chatgpt-diagram.png)

I then decided to use exactly the same prompt with Claude. This produced a much more useful diagram, here's [the Claude published version of the diagram](https://claude.site/artifacts/39c32052-3f09-42a1-aca1-33fbb01f637e).

![Claude generated software architecture diagram](/assets/images/posts/claude-diagram.png)

Interestingly Claude produced [Mermaid.js](https://mermaid.js.org/) code and presents both the code and a preview of the diagram next to the Chat UI.

![Claude UI screenshot](/assets/images/posts/claude-screenshot.png)

I wanted Claude to tweak the diagram, in particular the layout and colours. It struggled improving the layout, it did a much better job with the initial generation.

I then abandoned my AI approach and tried tweaking the layout using [mermaidchart.com](https://www.mermaidchart.com/) which has a GUI for editing Mermaid.js diagrams, I had limited success with this.

The best way to improve the layout would probably be to learn more about the [Mermaid.js syntax](https://mermaid.js.org/intro/syntax-reference.html) and tweak the code by hand.

If anyone can suggest good Mermaid.js graphic editing tools let me know, I suspect the use case for Mermaid.js is for relatively simple diagrams in developer documentation. Although their [architecture syntax](https://mermaid.js.org/syntax/architecture.html) looks promising.

To conclude I should have probably just made the diagram myself in something like Miro or Lucid Charts but where would the fun in that have been? I was impressed with Claude's ability to create diagrams, and pleasantly surprised by it's use of Mermaid.js, it still has some way to go with tweaking diagrams but will likely improve over time.