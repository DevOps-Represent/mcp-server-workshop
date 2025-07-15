
# 🧠 Part 2: More Tools & Prompt Engineering

Now let’s build out more of your MCP agent’s capabilities! In this section, we're going to create the following tools:

* 🏷️ get_animal_by_id
* 🐩 get_animal_by_name
* 🏡 adopt_pet

## 1. 🔍 Add get_animal_by_id

This tool lets Claude fetch a specific animal based on its ID.

🧠 What this tool does:

* Tool name: `get_animal_by_id`
* Input: `id` (like `cat-002`)
* Output: details about a single animal (or null if not found)
* Where to add it: Inside the `init()` method in your MyMCP class, just like `list_animals`

**Start the tool definition**

Below your list_animals tool inside the `init()` method, begin defining a new tool:  
‼️ Remember to put a great tool description to replace `TODO` ‼️

```ts
this.server.registerTool(
  "get_animal_by_id",
  {
    title: "Get an animal",
    description: "TODO",
```

**Add the input and output schemas**

This tool needs an input — the ID of the animal — and it will return an animal object (or null).

```ts
    inputSchema: {
      id: z.string()
    },
    outputSchema: {
      animal: z.nullable(animalSchema)
    }
  },
```

* ✅ z.string() means it expects a string (like "cat-002")
* ✅ z.nullable(...) means it’s okay if no animal is found — it returns null

**Now let’s tell the tool what to do when your mcp client calls it.**

The last part is to tell the tool what to do with the id.

```ts
  async ({ id }) => ({
    content: [{
      type: "text",
      text: JSON.stringify(this.animalRescueService.getAnimalById(id))
    }]
  })
);
```

<details>
<summary>🆘 Break Glass Code: get_animal_by_id</summary>

```ts
  this.server.registerTool(
   "get_animal_by_id",
   {
    title: "Get an animal",
    description: "Get an animal by id, only use this if you know the id of the animal",
    outputSchema: {
     animal: z.nullable(animalSchema)
    },
    inputSchema: {
     id: z.string()
    }
   },
   async ({ id }) => ({
    content: [{
          type: "text",
          text: JSON.stringify(this.animalRescueService.getAnimalById(id))
        }],
    structuredContent: { animal: this.animalRescueService.getAnimalById(id) }
   })
  );
```

</details>

### 🧪🐾  Testing

Test with a prompt like:

> “Can you show me the details for animal with ID cat-002?”

<details>
<summary>🐞 Common Errors + Debugging Tips</summary>

* ❌ z is not defined
  * Make sure you’re `importing z from "zod"` at the top of the file.
* ❌ animalSchema is not defined
  * Check that it’s imported from `"./animal-rescue-service"`.
* ❌ No result or empty response?
  * Confirm that the ID you’re testing actually exists in the dataset (check `animal-data.ts`)
* ❌ Claude/client says “no tools available”?
  * Make sure the tool is added inside the `init()`. Try restarting the client

</details>
<br>

## 2. 🐾 Add get_animal_by_name

Same idea, but matching by name.

🧠 What this tool does:

* Tool name: `search_animals_by_name`
* Input: the name of the animal (like "Charlie")
* Output: the animal’s full info if found, or null if it doesn’t exist
* Where to add it: Inside the `init()` method in your MyMCP class

**Start the tool definition**

Below your previous tool (or wherever you’re grouping your tools), begin writing:  
‼️ Remember to put a great tool description to replace `TODO` ‼️

```ts
this.server.registerTool(
  "search_animals_by_name",
  {
    title: "Get an animal",
    description: "Find an animal by name, only use this if you know the name of the animal",
```

**Add the input and output schemas**

This tool takes a name as input and tries to return a matching animal.

```ts
    inputSchema: {
      name: z.string()
    },
    outputSchema: {
      animal: z.nullable(animalSchema)
    }
  },
```

**Now let’s tell the tool what to do when your mcp client calls it.**

Now return the result from your animal service as plain text:

```ts
  async ({ name }) => ({
    content: [{
      type: "text",
      text: JSON.stringify(this.animalRescueService.getAnimalByName(name))
    }]
  })
);
```

<details>
<summary>🆘 Break Glass Code: get_animal_by_name</summary>

```ts
  this.server.registerTool(
   "search_animals_by_name",
   {
    title: "Get an animal",
    description: "Find an animal by name, only use this if you know the name of the animal",
    outputSchema: {
     animal: z.nullable(animalSchema)
    },
    inputSchema: {
     name: z.string()
    }
   },
   async ({ name }) => ({
    content: [{
          type: "text",
          text: JSON.stringify(this.animalRescueService.getAnimalByName(name))
        }],
    structuredContent: { animal: this.animalRescueService.getAnimalByName(name) }
   })
  );

```

</details>

### 🧪🐾  Testing

> “Can you show me the details for the dog Charlie?”

**👼🏻 We've done the work to ensure the dog name isn't case sensitive for you, try it out! 👼🏻**

## 3. 📝 Add adopt_pet Tool

Simulate an adoption — remove the pet from the list and return a message.

🧠 What this tool does:

* Tool name: `adopt_pet`
* Input: `id` (like `cat-002`)
* Output:
  * If successful, it returns a **certificate of adoption** and marks the action as **successful**.
  * If not, it returns `null` and sets `success` to `false`.
* Where to add it: Inside the `init()` method in your MyMCP class, just like `list_animals`

This tool builds on what you’ve done before, but introduces:

* A **boolean** `success` flag
* An optional **certificate** object (based on a schema)
* A slightly longer `run` function with some conditional logic

**Start the tool definition**

Begin in your `init()` method:

```ts
this.server.registerTool(
  "adopt_pet",
  {
    title: "Adopt a pet",
    description: "Adopt a pet by id, only use this if you know the id of the animal.",

```

**Add the input and output schemas**

This tool will:

* Take an id string as input
* Return a certificate (or null) and a success flag

```ts
    inputSchema: {
      id: z.string()
    },
    outputSchema: {
      certificate: z.nullable(adoptionCertificateSchema),
      success: z.boolean()
    }
  },
```

✅ adoptionCertificateSchema should already be imported from animal-rescue-service.ts.

**Now let’s tell the tool what to do when your mcp client calls it.**

We’ll:

1. Use your AnimalRescueService to attempt to adopt the pet
2. Check if it worked by seeing if we got back a certificate
3. Return that info as plain text (so your client can read it)

```ts
async ({ id }) => {
  const certificate = this.animalRescueService.adoptAnimal(id);
  const success = certificate !== null;

  return {
    content: [{
      type: "text",
      text: JSON.stringify({ certificate, success })
    }]
  };
}
```

This logic returns:

* A JSON-formatted string of the result
* A success flag to show whether the adoption happened
* A certificate object if successful, or null if not

<details>
<summary>🆘 Break Glass Code: adopt_pet</summary>

```ts
  this.server.registerTool(
   "adopt_pet",
   {
    title: "Adopt a pet",
    description: "Adopt a pet by id, only use this if you know the id of the animal, if the output is null there was an error. If a pet is not compatible with the customer, urge them to reconsider and adopt a more compatible pet.",
    outputSchema: {
     certificate: z.nullable(adoptionCertificateSchema),
     success: z.boolean()
    },
    inputSchema: {
     id: z.string()
    }
   },
   async ({ id }) => {
    const certificate = this.animalRescueService.adoptAnimal(id);
    const  success = certificate !== null;
    return {
     content: [{
            type: "text",
            text: JSON.stringify({
              certificate: certificate,
              success: success
            })
          }],
     structuredContent: { certificate: certificate, success: success }
    }
   }
  );
```

</details>  

### 🧪🐾  Testing

Test with a prompt like:

> “Adopt Cocoa”

## 4. 🧪 Run a Full Scenario (E2E)

Try this flow:

1. “List all available animals.”
2. “Tell me about Flopsy.”
3. “Okay, I’d like to adopt Flopsy.”

You should see Claude:

* Call list_animals
* Use get_animal_by_name
* Then adopt_pet

🙌 This is what tool orchestration looks like!

## 5. 🧠 Prompt Engineering

Refine the descriptions in your tools to guide Claude’s behavior.
Try things like:

`“Only return the pet’s name, type, and personality. No extra text.”`

or

`“Make recommendations based on compatibility with young children.”`

Your prompt is your agent’s operating system — tweak it and test!

🎉 Great job on getting this far!!

## Let's try this as a hosted option using Cloudflare
