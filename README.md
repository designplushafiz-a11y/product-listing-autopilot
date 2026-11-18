# Product Listing Autopilot (Lite) — Claude Skill

Free lite edition of **Product Listing Autopilot**, a Claude skill that lists apparel products (t-shirts, hoodies) on an e-commerce admin panel from a folder of mockup images.

## What's in Lite (free)

- `references/content-rules.md` — SEO copywriting rules: one universal title across all colours, short/long description, meta description, SEO title, keywords
- `scripts/audit_folder.py` — checks a product image folder before listing (missing front images, missing colour folders, wrong counts, stray files)

```
python3 scripts/audit_folder.py "<path to SKU folder>"
```

Expected folder structure:

```
<SKU>/
  BLACK/ WHITE/ RED/ GREY/ NAVY/
    01_FRONT  02_BACK  03_SIDE  04_GALLERY  05_MODEL  06_CART  07_FABRIC_MICRO
```

## Full version (paid)

The full skill does the whole listing end to end. You only give the folder name and drag the folder into the browser once:

- Writes all SEO content from the design
- Creates the product, specs, prices and every colour × size variant with stock
- Uploads every image to the correct slot for every colour
- Writes 7 detailed, full-width A+ content blocks
- Verifies counts and sends the product for approval
- Flags trademark, placeholder-text and size-chart issues
- Handles revisions without duplicate images

**Get the full version or a done-for-you setup for your store:** contact via Fiverr — https://www.fiverr.com/atexsell

## Notes

- Claude never types passwords; you log in yourself.
- You are responsible for having the rights to every design you sell.
