# Web3 Learning Path - Beginner (Solidity Refresher)

> 1-2 hours/day - You have touched Solidity before, so this is a refresher plus a small step into real tooling.

---

## Day 1 - Solidity Refresher
**Goal:** get the syntax back in your head.

- Data types: `uint`, `address`, `bool`, `string`, `bytes`
- State variables vs local variables
- Functions: `public`, `private`, `view`, `pure`
- Constructor

**Practice:** write a simple `Counter` contract that stores a number, increments it, and reads it.

Resources:
- [docs.soliditylang.org](https://docs.soliditylang.org) - official docs
- [cryptozombies.io](https://cryptozombies.io) - interactive refresher

---

## Day 2 - Mappings, Structs, Events, Modifiers
**Goal:** understand the building blocks used in real contracts.

- `mapping(address => uint)` - the key data structure in Solidity
- Structs - grouping related data
- Events - logging things on-chain
- Modifiers - reusable access control, for example `onlyOwner`

**Practice:** extend your `Counter` so only the deployer can increment it, and emit an event each time.

---

## Day 3 - Setup Hardhat + Run Locally
**Goal:** get off the browser and into a real dev environment.

```bash
mkdir hardhat-counter
cd hardhat-counter
npm init -y
npm install --save-dev hardhat
npx hardhat --init
```

- Choose a basic Hardhat project and accept the defaults if you are unsure.
- Understand the project structure: `contracts/`, `test/`, `scripts/` or `ignition/`
- Compile your contract: `npx hardhat compile`
- Run the sample tests first: `npx hardhat test`

**Optional local network:**

Open one terminal:

```bash
npx hardhat node
```

Open another terminal to deploy or run scripts against the local node.

**Focus:** do not worry about testnets yet. Fake local accounts are enough for this 5-day plan.

---

## Day 4 - Testing Your Contracts
**Goal:** learn to catch mistakes before deploying anything that involves real money.

- Start from the sample test Hardhat generated.
- Test your `Counter`: deploy it, call functions, and assert the result.
- Run: `npx hardhat test`

**Focus:** keep the test simple. One passing test that you understand is better than five copied tests.

---

## Day 5 - ERC-20 Token Standard
**Goal:** understand the most common smart contract standard.

- What is ERC-20 - the interface most tokens follow
- Use OpenZeppelin - do not reinvent the wheel

```bash
npm install @openzeppelin/contracts
```

```solidity
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor() ERC20("MyToken", "MTK") {
        _mint(msg.sender, 1000 * 10 ** decimals());
    }
}
```

- Deploy it locally
- Check your balance
- Transfer between test accounts

**Focus:** understand what `_mint`, `balanceOf`, and `transfer` mean. Gas optimization can wait.

---

## After the 5 days
- ERC-721 (NFTs)
- DeFi concepts - liquidity pools, AMMs
- Connecting contracts to a frontend with ethers.js or viem
