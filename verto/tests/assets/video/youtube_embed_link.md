## Run Length Encoding

{video url="https://www.youtube.com/embed/uaV2RuAJTjQ?rel=0"}

Run length encoding (RLE) is a technique that isn't so widely used these days, but it's a great way to get a feel for some of the issues around using compression.

{panel type="teacher-note" summary="Who uses run length encoding?"}

[Run-length_encoding](https://en.wikipedia.org/wiki/Run-length_encoding) was widely used when black and white images were the norm.
One of its key roles was as the compression method that made Fax (facsimile) machines possible in a standard that was adopted in 1980.
The pixels in a fax image are only black or white, and typically there are long runs of white pixels in the margins, so RLE is particularly effective.
Also, the method is very simple, and in the 1980s this was important since it reduced the cost of the electronics inside the machine.

Run length encoding is still used as part of JPEG compression, although not to code runs of pixels (in a photo it's unusual to have runs of exactly the same colour).

We have introduced RLE here because it is a practical approach to compression, and most importantly it shows the key benefits and problems that arise in compression.

{panel end}
