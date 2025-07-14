
# 🛠️ Workshop Setup Instructions

This guide will help you get ready to build and deploy your MCP server using Claude and the MCP SDK. These instructions are platform-agnostic — you can use **any operating system** and **any code editor or IDE** you like (VS Code, JetBrains, Vim, etc.).

We’ll link to official install guides where needed to keep things simple and up-to-date.

---

<details>
<summary><strong>0. Pick your favourite Code Editor</strong></summary>

To follow along this workshop, you will need a code editor such as VS Code, IntelliJ, Cursor or vim.

</details>

---

<details>
<summary><strong>1. Install Node.js (for TypeScript users)</strong></summary>

You’ll need **Node.js v18+** to use the TypeScript MCP SDK and deploy to Cloudflare.

👉 [Install Node.js](https://nodejs.org/en/download)

After installation, confirm it's working:

```bash
node -v
npm -v
```

</details>

---

<details>
<summary><strong>2. Install Python (for Python users)</strong></summary>

You’ll need **Python 3.10+** to use the Python MCP SDK.

👉 [Install Python](https://www.python.org/downloads/)

After installation, confirm it's working:

```bash
python --version
```

(You may need to use `python3` on some systems.)

</details>

---

<details>
<summary><strong>3. Set Up Git and GitHub</strong></summary>

We’ll be cloning and pushing code via GitHub. You’ll need:

- A **GitHub account** → [Sign up here](https://github.com/signup)
- Git installed locally → [Install Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

To check if Git is installed:

```bash
git --version
```

</details>

---

<details>
<summary><strong>4. Pick your favourite MCP client </strong></summary>

We’ll be using Claude and will take advantage of their free tier, alternatively you can use the [cloudflare playground](https://playground.ai.cloudflare.com/) + `llama-4-scout-17b-16e-instruct` model.

👉 [Create a Claude account](https://claude.ai/)

<!-- TODO: add instructions for other major MCP client -->

</details>

---

<details>
<summary><strong>5. Install a Package Manager</strong></summary>

**TypeScript users:** Use `npm` or `pnpm` (comes with Node.js).  
<!-- TODO: decide whether we'll be using pip or uv -->
**Python users:** Use `pip` or `pipenv`.

To check:

```bash
# For TS
npm -v
pnpm -v

# For Python
pip --version
```

(You may need to use `pip3` on some systems.)

If needed:  
👉 [Install pip](https://pip.pypa.io/en/stable/installation/)  
👉 [Install pipenv](https://pipenv.pypa.io/en/latest/)
<!-- TODO: instructions for uv -->

</details>

---

<details>
<summary><strong>6. Set Up Cloudflare for Deployment (Optional)</strong></summary>

You’ll be deploying your MCP server using **Cloudflare Workers** or **Pages Functions**.

- Sign up here: 👉 [Create a free Cloudflare account](https://dash.cloudflare.com/sign-up)
- Install the Cloudflare CLI (`wrangler`) → [Install Wrangler](https://developers.cloudflare.com/workers/wrangler/install-and-update/)

To test:

```bash
npx wrangler --version
// or
npx wrangler version
// or
npx wrangler -v
```

We’ll walk through the rest in the workshop.

</details>

---

<details>
<!-- TODO: remove if we don't manage to test and set this up -->
<summary><strong>7. (Optional) Use Gitpod or Codespaces</strong></summary>

If you’d prefer not to install anything locally, you can use a cloud dev environment:

- [Gitpod](https://gitpod.io) – auto launches from `.gitpod.yml`
- [GitHub Codespaces](https://github.com/features/codespaces) – available for many users on GitHub

We’ll provide a Gitpod link in the starter repo.

</details>

---

<details>
<summary><strong>✅ Checklist Before You Arrive</strong></summary>

- [ ] A Code editor
- [ ] Node.js **v18+** OR Python **3.10+** installed  
- [ ] Git installed + GitHub account ready  
- [ ] Ensure you have an MCP Client ready
- [ ] Code editor installed (VS Code, etc.)
- [ ] Cloudflare account created  
- [ ] Optional: Gitpod/Codespaces working  

Need help? Don’t stress — we’ll be available to troubleshoot during the workshop!

</details>
