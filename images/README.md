# images/

The site currently uses pure-CSS product art, so it works with this folder empty.

When you're ready to use real product photos, drop them here (suggested names):

- `grape-cluster.jpg` — grape soap on jute rope
- `rice-rose.jpg` — Rice Water & Rose bar + box
- `orange-honey.jpg` — Orange Peel & Honey bar + box
- `neem-mugwort.jpg` — Neem & Mugwort bar
- `batch.jpg` — full table of soaps (great for the Our Story section)
- `gift-box.jpg` — kraft gift boxes with ribbon

Then in the HTML, replace a `.soap-visual` div's contents with:
`<img src="images/grape-cluster.jpg" alt="Grape Cluster Soap" style="width:100%;height:100%;object-fit:cover">`

Keep photos under ~300 KB each (resize to ~1200px wide) so the site stays fast.
