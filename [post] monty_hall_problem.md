I was **extremely** disappointed that a unit that went into an extraordinary level of detail of Bayes nets, inference, sampling, etc., referred to the Monty Hall problem as an obligatory curiosity and then answered it by saying "I'm so, so very clever, bite me Monty."

Rather than just moan, this is my process of applying Bayes nets to the Monty Hall problem. I've marked this as a community wiki; please feel free to edit, update, append, etc. Also, I might be completely wrong about much of my reasoning; tell me!

- - -

I want to draw a Bayes net representing the Monty Hall problem. Nodes are random variables, so what are the random variables?

-    Before I make a choice the prize exists behind some door. Let's call this `Prize (P)`, which is discrete and may have values `[Door1, Door2, Door3]`
-    I choose a door at the beginning. Let's call this `First selection (F)`, which is discrete and may have values `[Door1, Door2, Door3]`. 
-    Monty, the host, opens a door. Let's call this `Monty opens (M)`, which is discrete and may have values `[Door1, Door2, Door3]`.

What are the edges?

-    Where the `Prize` is will affect which door `Monty opens`; he'll never open the door the `Prize` is behind! Hence `P -> M`.
-    Which door I open will affect which door Monty opens. He can't re-open the door I've just opened! Hence `F -> M`.

Interesting...this looks familiar. This looks like a particular triplet covered in the "D Separation (3.35)" unit! This triplet tells us:

1.    `P` and `F` are **absolutely independent**. In the absence of other information they do not provide information about one another. (This makes sense!)
2.    `P` and `F` are **conditionally dependent on M**. Given M there is a link between `P` and `F`.

For me, point 2 is mind-blowing! There is a connection between `P` and `F` in the Bayes net, whereas every ounce of intution in my mind asserts that there is absolutely no connection between the two. *Without even doing any calculations* we've just discovered something totally unintuitive about the Monty Hall problem.

I think we're going to need four tables, drawn out below:

    +---------+  +---------+
    |  P(F)   |  |  P(P)   |
    +---------+  +---------+
    | D1 | 1/3|  | D1 | 1/3|
    |----|----|  |----|----|
    | D2 | 1/3|  | D2 | 1/3|
    |---------|  |---------|
    | D3 | 1/3|  | D3 | 1/3|
    +----v----+  +----v----+

    +--------------+   +--------------+
    |  P(M|F)      |   |  P(M|P)      |
    |---+---+------+   |---+---+------+
    | M | F |      |   | M | P |      |
    |---|---|------|   |---|---|------|
    | D1| D1|  0   |   | D1| D1|  0   |
    |--------------|   |--------------|
    | D1| D2|  1/2 |   | D1| D2|  1/2 |
    |--------------|   |--------------|
    | D1| D3|  1/2 |   | D1| D3|  1/2 |
    |--------------|   |--------------|
    | D2| D1|  1/2 |   | D2| D1|  1/2 |
    |--------------|   |--------------|
    | D2| D2|  0   |   | D2| D2|  0   |
    |--------------|   |--------------|
    | D2| D3|  1/2 |   | D2| D3|  1/2 |
    |--------------|   |--------------|
    | D3| D1|  1/2 |   | D3| D1|  1/2 |
    |--------------|   |--------------|
    | D3| D2|  1/2 |   | D3| D2|  1/2 |
    |--------------|   |--------------|
    | D3| D3|  0   |   | D3| D3|  0   |
    +--------------+   +--------------+

Keep in mind the constraints of the problem: Monty cannot re-open the door I opened, and Monty will never open the door with the prize behind it.

Also, I think, given that M has two incident edges, we actually need a `P(M | F,P)` table, but to save space I've excluded it and used intuition in its place.

Suppose I've chosen D1, then Monty chooses D3 - just like the lecture video. Should we switch? Well:

$$\alpha \buildrel\triangle\over = P(P = D1 | F = D1, M = D3)$$
$$\beta \buildrel\triangle\over = P(P = D2 | F = D1, M = D3)$$

If $$\beta \gt \alpha$$ then we should switch. Else we should not switch. In English, beta is "If I chose D1, and Monty chose D3, is the prize behind D2?".

Rather than go to the trouble of calculating alpha, we just note that:

$$\alpha + \beta = 1$$

This is true because of the contraints of the problem; Monty will never reveal the door containing the prize, hence the prize may only be behind doors D1 or D2.

Hence, we are actually trying to determine if:

$$\beta \gt \frac{1}{2}$$

Using conditional probability:

$$\beta = \frac{P(P=D2, F=D1, M=D3)}{P(F=D1, M=D3)}$$

Using material from Section 4.2 (Enumeration):

$$\beta = \frac{P(P=D2) \times P(F=D1) \times P(M=D3 | P=D2, F=D1)}{P(F=D1) \times P(M=D3 | F=D1)}$$

$$\beta = \frac{\frac{1}{3} \times \frac{1}{3} \times P(M=D3 | P=D2, F=D1)}{\frac{1}{3} \times P(M=D3 | F=D1)}$$

The conditional in the denominator can be read straight out of the `P(M|F)` table:

$$\beta = \frac{\frac{1}{3} \times \frac{1}{3} \times P(M=D3 | P=D2, F=D1)}{\frac{1}{3} \times \frac{1}{2}}$$

$$\beta = \frac{2}{3} \times P(M=D3 | P=D2, F=D1)$$

That leaves the conditional:

$$\gamma \buildrel\triangle\over = P(M=D3 | P=D2, F=D1)$$

$$\beta = \frac{2}{3} \times \gamma$$

Pause and consider what gamma actually is. If I choose D1, and the prize is behind D2...what door will Monty choose?

-    D1? No! It's already open.
-    D2? No! The prize is behind there.
-    D3? Yes.

**Monty will always choose D3**!

$$\gamma = 1$$

$$\beta = \frac{2}{3}$$

QED.