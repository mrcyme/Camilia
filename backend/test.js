/*
create a choas function plot

*/
/*
To create a chaos function plot in JavaScript, you can use the HTML5 canvas element to draw the plot. The chaos function typically involves iterating a mathematical function multiple times. Here's an example of a chaos function plot using the logistic map:



In this example, we use the logistic map as the chaos function. The logistic map is a mathematical function that can generate chaotic behavior. Adjust the value of the `r` variable to modify the chaos pattern. The canvas element is used to plot the chaos function. The function `chaosFunctionPlot` iterates the logistic map multiple times and plots the points on the canvas. The canvas dimensions and scales are configured to fit the plot properly.
*/
<!DOCTYPE html>
<html>
  <head>
    <style>
      canvas {
        border: 1px solid black;
      }
    </style>
  </head>
  <body>
    <canvas id="chaosCanvas" width="600" height="400"></canvas>

    <script>
      // Create a chaos function plot using the logistic map
      function chaosFunctionPlot() {
        const canvas = document.getElementById("chaosCanvas");
        const ctx = canvas.getContext("2d");

        const width = canvas.width;
        const height = canvas.height;
        const xScale = width / 4;
        const yScale = height;

        const iterations = 10000;
        const r = 3.7; // Adjust this for different chaos patterns
        let x = 0.5;

        // Iterate the logistic map multiple times and draw the plot
        for (let i = 0; i < iterations; i++) {
          const px = i * width / iterations;
          const py = height - x * yScale;

          ctx.fillRect(px, py, 1, 1);

          x = r * x * (1 - x);
        }
      }

      // Call the chaos function plot
      chaosFunctionPlot();
    </script>
  </body>
</html>
