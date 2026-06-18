# Web3 Learning Path — Beginner (Solidity Refresher)

> 1–2 hours/day · You've touched Solidity before so this is a refresher + building on top

---

## Day 1 — Solidity Refresher
**Goal:** get the syntax back in your head

- Data types: `uint`, `address`, `bool`, `string`, `bytes`
- State variables vs local variables
- Functions: `public`, `private`, `view`, `pure`
- Constructor

**Practice:** write a simple `Counter` contract — store a number, increment it, read it.

Resources:
- [docs.soliditylang.org](https://docs.soliditylang.org) — official docs
- [cryptozombies.io](https://cryptozombies.io) — interactive refresher

---

## Day 2 — Mappings, Structs, Events, Modifiers
**Goal:** understand the building blocks of real contracts

- `mapping(address => uint)` — the key data structure in Solidity
- Structs — grouping related data
- Events — logging things on-chain
- Modifiers — reusable access control (`onlyOwner`)

**Practice:** extend your Counter — only allow the deployer to increment, emit an event each time.

---

## Day 3 — Setup Hardhat + Deploy Locally
**Goal:** get off the browser and into a real dev environment

```bash
npm init -y
npm install --save-dev hardhat
npx hardhat init
```

- Understand the project structure: `contracts/`, `scripts/`, `test/`
- Compile your contract: `npx hardhat compile`
- Deploy locally: `npx hardhat run scripts/deploy.js --network localhost`
- Use the fake ETH accounts Hardhat gives you

**Focus:** this is what you used before — Hardhat's local network with fake ETH.

---

## Day 4 — Testing Your Contracts
**Goal:** learn to write tests so you catch bugs before deploying real money

- Write tests in JavaScript using ethers.js + Hardhat
- Test your Counter: deploy it, call functions, assert results
- Run: `npx hardhat test`

**Focus:** on-chain bugs can't be patched after deploy — testing is non-negotiable in Web3.

---

## Day 5 — ERC-20 Token Standard
**Goal:** understand the most common smart contract standard

- What is ERC-20 — the interface every token follows
- Use OpenZeppelin — don't reinvent the wheel

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

- Deploy it locally, check balances, transfer between test accounts

---

## After the 5 days
- ERC-721 (NFTs)
- DeFi concepts — liquidity pools, AMMs
- Connecting contracts to a frontend with ethers.js or viem
