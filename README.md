# Dio

A rather tenuous name. Branding functions with a "created by AI" message and attributes to help identify them.

Brand -> Brando -> Dio Brando -> Dio -> [Za Warudo](https://jojo.fandom.com/wiki/The_World)


## Installation

Don't for now. I'll bundle up all the different languages into branches later.

## Usage

### Python

Decorate your functions with `@copilot`. This is explicitly copilot as that's the tool available in a work setting for me. Other LLM origins are not supported *yet*.

This provides:

- A warning that a function call is using a function which was written with or by Microsoft Copilot, including the function call itself.
- Attributes to the function itself to better frame your questions when investigating the content.
  + Code complexity (via cyclomatic complexity computation)
  + Identification of long line and deeply nested (list + conditional) anti-patterns
  + System information for the system on which the function is called

