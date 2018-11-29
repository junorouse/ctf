# EOSGame

- Target contract makes random values using vulnerable variables(block.number, block.timestamp).
- You may think that attacker cannot guess the timestamp when the block is made.
- But when attacker call a contract via contract(internal call, internal tx), attacker can simply guess the random values and always win.

