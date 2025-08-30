
---

## Deployment

### Dash Apps (Render)
- Both Dash apps are wrapped by a Flask server (`multi.py`) and deployed to Render.  
- Render runs the service with Gunicorn (`multi:server`) as defined in `render.yaml`.  
- Accessible at:  
  - Earnings Level Gap → [https://divergent-paths-7.onrender.com/level/](https://divergent-paths-7.onrender.com/level/)  
  - Earnings Rank Gap → [https://divergent-paths-7.onrender.com/rank/](https://divergent-paths-7.onrender.com/rank/)
    (because it took me 7 attempts to correctly deploy)

### Static Website (GitHub Pages)
- The `docs/` folder is published via GitHub Pages.  
- It contains a scrollytelling narrative that embeds the Dash apps using `<iframe>`.  
- Accessible at:  
  - [https://charooanand.github.io/divergent-paths/](https://charooanand.github.io/divergent-paths/)

---

## Tech Stack

- **Dash** (Plotly + React) for interactive histograms.  
- **Flask** to host multiple Dash apps under one server.  
- **Gunicorn** production WSGI server (on Render).  
- **scrollama.js** for the scrollytelling narrative.  
- **GitHub Pages** for static site hosting.  

---

## Citation

Bayer, P., & Charles, K. K. (2018). *Divergent paths: A new perspective on earnings differences between black and white men since 1940*.  
The Quarterly Journal of Economics, 133(3), 1459–1501.
