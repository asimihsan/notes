# notes

There are just notes I've made when reading up on languages, frameworks, sites, or books.

After starting a few Coursera courses I realised I needed both Markdown and LaTeX support. To that end I've created a simple script that uses `pandoc` to do the necessary conversion, i.e.

		pandoc <filename.md> -o tex/<filename.tex>
		
Conversion to TeX leaves LaTeX statements bounded by `$$ .. $$` intact; super! Open the TeX file in TexShop, which should handle regeneration to PDF for you.