# EB-2 NIW Project Summary — Agentic AI Fraud Defense Framework

## Project purpose

This software project demonstrates an executable implementation of a published framework for AI-driven financial fraud detection, investigation, and risk mitigation in real-time payment environments.

The prototype focuses on the engineering problem identified in the underlying paper: in instant-payment systems, fraud defense must move beyond isolated transaction scoring and integrate **detection, explanation, investigation, response, governance, and learning** within a tightly orchestrated loop.

## Technical contribution demonstrated by the repository

The implementation converts the framework into five software layers:

- real-time transaction ingestion;
- online feature computation and graph-based relationship analysis;
- multi-signal detection and explainable reasoning;
- specialized triage, investigation, and response agents;
- human-governed policy enforcement and auditable decisions.

The project also demonstrates a **Sense → Reason → Decide → Act → Learn** lifecycle and provides hooks for replacing research-prototype scorers with production ML, sequence, and graph models.

## Relevance to financial-system resilience

The system is designed around fraud typologies discussed in the framework, including account takeover, authorized push-payment fraud, synthetic identity risk, card-not-present fraud, mule-network activity, and abuse of real-time payment rails.

The prototype is particularly focused on:
- reducing the time between detection and mitigation;
- improving the evidence available to fraud analysts;
- supporting explainable decision-making;
- bounding autonomous actions through governance;
- preserving human authority over high-impact decisions.

## Evidence that can be shown in a petition package

A petitioner can document this project with:
- the peer-reviewed paper;
- GitHub repository URL;
- repository release/tag;
- architecture diagram;
- screenshots of Swagger/API responses;
- sample audit record;
- demo execution output;
- test results / CI status;
- commit history;
- technical documentation;
- future benchmark or pilot results.

## Important representation note

This repository should be described accurately as a **research prototype / reference implementation** unless and until it is independently benchmarked or deployed. The underlying paper explicitly characterizes its evaluation figures as illustrative rather than measurements from a live, fielded system. Any petition statement should distinguish:
1. the published conceptual contribution;
2. this executable implementation;
3. any later empirical validation or production deployment.

That distinction makes the evidence more credible and avoids overstating the state of the work.
