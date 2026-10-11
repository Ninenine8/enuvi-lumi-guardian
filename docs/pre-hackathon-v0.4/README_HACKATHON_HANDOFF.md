# Lumi Guardian — Hackathon Handoff
Last consolidated: October 2026

## What this pack is

This folder is a handoff for continuing **Lumi Guardian / ENUVI** in another ChatGPT conversation without re-explaining the project.

## Project

**Lumi** is the first physical prototype of ENUVI, an embodied AI companion being built under **MadeByNeon** in Singapore.

The hackathon/public-safe slice is **Lumi Guardian**: a safety layer for an AI companion that can remember, reason and eventually take real-world actions.

Core question:

> Just because an AI can do something, should it be allowed to?

Guardian is about **controlled agency**. It separates:
- access permission
- disclosure permission
- action permission
- transaction-specific confirmation

Core line:

> **The goal isn't to make AI less capable. It's to make capability accountable to user intent.**

Useful architecture line:

> **Gemini reasons. Guardian governs. Tools execute.**

## Public build

Article:
**https://madebyneon.com/lumi-guardian/**

Public title:
**Building Lumi Guardian**

Subtitle:
**Making an AI companion useful without giving it unlimited authority.**

## Physical Lumi

Current prototype direction includes:
- ESP32-S3-class controller
- 1.28-inch round 240×240 display
- Wi-Fi / Bluetooth
- microphones + speaker
- physical mic kill switch
- presence sensing
- compact physical embodiment

The final video in this folder uses the **real bench prototype** and the builder's real voice.

## Why Guardian matters

As an AI gains access to memory, messages, payments, sensors, communications and external tools, simple blanket permission is not enough.

Ageing and caregiving are important use cases, especially in Singapore, but Lumi is **not positioned as only an elder-care device**. The larger problem is trusted AI assistance in everyday life.

## Strongest demo story

The strongest Guardian story is **Test 4**.

The model correctly reasoned that a current $800 transfer could be allowed after explicit confirmation, while a casual request to automatically approve future transfers should not create permanent authority.

But it then falsely said:

> “I have processed the $800 transfer.”

No trusted external service had confirmed that.

That exposed a deeper problem:
**correct reasoning is not enough if the AI invents real-world state.**

Guardian therefore added explicit action-state tracking:

**AUTHORIZED → INITIATED → COMPLETED**

This is a strong hackathon demo because it shows:
**problem → test → failure → rule change → retest → stronger system**

## Hackathon scope

Do NOT try to expose the entire ENUVI architecture.

Keep the hackathon focused on:
- Guardian reasoning
- permission boundaries
- action-state integrity
- memory vs authority
- prompt-injection resistance
- emergency handling
- one clear end-to-end demo
- real Lumi hardware as embodiment/proof

A strong demo flow:
1. user asks Lumi to do something consequential;
2. Gemini reasons about the request;
3. Guardian evaluates permissions, evidence and action state;
4. Guardian outputs ALLOW / ASK_CONFIRMATION / BLOCK / ESCALATE;
5. action state remains explicit;
6. Lumi explains the decision naturally;
7. optional physical Lumi display reacts to the decision/state.

## Tech positioning

Public-safe positioning:
- **Gemini** = reasoning component
- **Guardian** = safety / authority layer
- **Tools / services** = real-world action execution
- **Lumi hardware** = physical embodiment

Do not claim Google endorses or partners with ENUVI.

Safe wording:
> “Gemini is currently used as the reasoning component in the Guardian prototype.”

Guardian should remain model-independent in architecture.

## Files in this pack

- `00_PASTE_THIS_IN_NEW_CHAT.txt`
- `01_madebyneon-v1.1.7.zip` — full MadeByNeon site with Lumi Guardian page
- `02_lumi-guardian-final-video.mp4` — final ~57-second voiceover video
- `03_lumi-guardian-thumbnail.jpg`
- `04_original-voiceover.m4a`
- `GUARDIAN_V0.4_BASELINE.md`
- `TESTS_01_TO_21.md`
- `README_HACKATHON_HANDOFF.md`

## Working style for the next chat

- Continue from this pack rather than restarting ideation.
- Keep Guardian v0.4 frozen unless deliberately creating a separately versioned v0.5.
- Distinguish demo shortcuts from production architecture.
- Do not overclaim hardware, sensor or tool capabilities.
- Prioritize a working end-to-end hackathon demo over adding more speculative features.
- Preserve MadeByNeon visual direction: warm off-white, charcoal/black structure, neon-lime accent, rounded cards, whitespace, clean/playful product-studio feel.
