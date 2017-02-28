You can try out this 3D matrix in the following interactive.

{button-link link="http://www.csfieldguide.org.nz/releases/1.9.9/_static/widgets/CG/CG-mini-editor/main%20(cutdown).html?info=%0AIn%20this%20interactive,%20try%20changing%20the%20scaling%20on%20the%20image%20(it%20starts%20with%20a%20scaling%20factor%20of%2010%20in%20all%20three%20dimensions)." text="Click for interactive: 3D transform matrix"}

The above image mesh has 3644 points in it, and your matrix was applied to each one of them to work out the new image.

The next interactive allows you to do translation (using a vector).
Use it to get used to translating in the three dimensions (don't worry about using matrices this time.)

{button-link link="http://www.csfieldguide.org.nz/releases/1.9.9/_static/widgets/CG/CG-mini-editor/main%20(cutdown).html?info=%0ATranslation%20requires%203%20values,%20which%20are%20added%20to%20the%20*x*,%20*y*%20and%20*z*%20coordinates%20of%20each%20point%20in%20an%20object.%3Cp%3EIn%20the%20following%20interactive,%20try%20moving%20the%20teapot%20left%20and%20right%20(%20%3Cem%3Ex%3C/em%3E%20),%20up%20and%20down%20(%20%3Cem%3Ey%3C/em%3E%20),%20and%20in%20and%20out%20of%20the%20screen%20(%20%3Cem%3Ez%3C/em%3E%20)%20by%20adding%20a%20%E2%80%9Cvector%E2%80%9D%20to%20the%20operations.%20Then%20try%20combining%20all%20three.%3C/p%3E%0A" text="Click for interactive: 3D translation"}

Rotation is trickier because you can now rotate in different directions.
In 2D rotations were around the centre (origin) of the grid, but in 3D rotations are around a line (either the horizontal x-axis, the vertical y-axis, or the z-axis, which goes into the screen!)

The 2D rotation we used earlier can be applied to 3 dimensions using this matrix:

{button-link link="http://www.csfieldguide.org.nz/releases/1.9.9/_static/widgets/CG/CG-mini-editor/main%20(cutdown).html?info=%0AYou%20can%20experiment%20with%20moving%20the%20teapot%20around%20in%20space,%20changing%20its%20size,%20and%20angle.%3Cdl%20class=%22docutils%22%3E%0A%3Cdt%3EThink%20about%20the%20order%20in%20which%20you%20need%20to%20combine%20the%20transforms%20to%20get%20a%20particular%20image%20that%20you%20want.%3C/dt%3E%0A%3Cdd%3EFor%20example,%20if%20you%20translate%20an%20image%20and%20then%20scale%20it,%20you%E2%80%99ll%20get%20a%20different%20effect%20to%20scaling%20it%20then%20translating%20it.%0AIf%20you%20want%20to%20rotate%20or%20scale%20around%20a%20particular%20point,%20you%20can%20do%20this%20in%20three%20steps%20(as%20with%20the%202D%20case%20above):%20(1)%20translate%20the%20object%20so%20that%20the%20point%20you%20want%20to%20scale%20or%20rotate%20around%20is%20the%20origin%20(where%20the%20x,%20y%20and%20z%20axes%20meet),%20(2)%20do%20the%20scaling/rotation,%20(3)%20translate%20the%20object%20back%20to%20where%20it%20was.%20If%20you%20just%20scale%20an%20object%20where%20it%20is,%20its%20distance%20from%20the%20origin%20will%20also%20be%20scaled%20up.%3C/dd%3E%0A%3C/dl%3E%0A" text="Click for interactive: 3D with multiple matrices and vectors"}

In the above examples, when you have several matrices being applied to every point in the image, a lot of time can be saved by converting the series of matrices and transforms to just one formula that does all of the transforms in one go. The following interactive can do those calculations for you.

For example, in the following interactive, type in the matrix for doubling the size of an object (put the number 2 instead of 1 on the main diagonal values), then add another matrix that triples the size of the image (3 on the main diagonal). The interactive shows a matrix on the right that combines the two --- does it look right?

{button-link link="http://www.csfieldguide.org.nz/releases/1.9.9/_static/widgets/CG/CG-matrix-simplifier/CG-matrix-simplifier.html?info=Multiple%20transforms" text="Click for interactive: matrix simplifier"}
