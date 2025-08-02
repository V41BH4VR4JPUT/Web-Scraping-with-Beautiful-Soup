# LEARNING_LOG.md

##  Part 1 Reflection: Wikipedia Article Navigator

###  HTML Elements and Attributes Used
- **First Paragraph**: I inspected the `div` with ID `mw-content-text`, and searched for the first `<p>` tag that contained non-empty text. These are usually located directly under the main title and before any `<h2>` subheadings.
- **External Links**: I targeted `<h2>` or `<h3>` headers with text like "External links". Then, I navigated to the next `<ul>` (unordered list) using `find_next_sibling()`. Inside that list, I extracted `<a>` tags with `href` attributes that started with `http`.
- **Subheadings**: Subheadings are consistently structured as `<h2>`, `<h3>`, and `<h4>` tags inside the same `div#mw-content-text`. I collected these using `find_all()` with a list of tags.

###  Strategy for “See Also” Links
To extract internal links from the "See also" section:
1. I looked for headers (`<h2>`, `<h3>`) with the exact text "See also".
2. I then navigated to the following `<ul>` and looped through each `<li>` to extract `<a>` tags.
3. I filtered links to include only those with `href` starting with `/wiki/`, indicating internal Wikipedia links.

###  Handling the “Follow a ‘See Also’ Link” Challenge
After listing the "See also" links, I added user input functionality to choose a specific article by number. If the user chose one:
- I extracted the URL and recursively passed it to the same scraping function.
- Considerations:
  - Prevent infinite loops by allowing navigation only once.
  - Handle invalid input gracefully using `try/except`.

---

##  Part 2 Reflection: Blog Explorer – DEV.to

###  Target Blog: [https://dev.to](https://dev.to)

###  HTML Structure Targeted
- I used browser dev tools (`Inspect Element`) and noticed that each article on the homepage is wrapped in a link (`<a>`) tag with:
  - `class="crayons-story__hidden-navigation-link"`
- These `<a>` tags have:
  - The **title** as the text content.
  - The **URL** as a relative link in the `href` attribute.

###  HTML Snippet Example:
```html
<a href="/someauthor/some-article-title" class="crayons-story__hidden-navigation-link">
    Some Article Title
</a>
