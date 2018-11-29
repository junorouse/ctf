# Fake3D

- The main idea of this challenge is same as EOSGame.
- But there is two different things.

## Check callers are normal address or contract?

```solidity
modifier turingTest() {
	address _addr = msg.sender;
	uint256 _codeLength;
	assembly {_codeLength := extcodesize(_addr)}
	require(_codeLength == 0, "sorry humans only");
	_;
}
```

- Attacker can bypass `require codeLength` by using a constructor code of contract. (See the exploit.sol)


## Validation address and winning point.

- https://ropsten.etherscan.io/tx/0x6a514d4ea5cffc96d211f6658a0128943909415af326759ff86bee47e3d63f8f
- Transaction has reverted even I have token more than 8888.
- I want to know why, but I don't have much time to debug. (I have to sleep :D)
- I guess there was a calculation with address and token amount.
- So I changed address some times, then transaction called `CaptureTheFlag` function successfully.
