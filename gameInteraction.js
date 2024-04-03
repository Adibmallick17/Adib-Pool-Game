// document.addEventListener('DOMContentLoaded', function() {
//     // Get the cueball element from the SVG
//     var cueball = document.getElementById('cueBall');
//     var line = document.getElementById('line');

//     line.setAttribute('x1', cueball.cx.baseVal.value);
//     line.setAttribute('y1', cueball.cy.baseVal.value);

//     // Variables to track mouse coordinates and dragging state
//     var isDragging = false;
//     var initX, initY; // Define initX and initY outside of the event listeners

//     // Add mousedown event listener to start dragging
//     cueball.addEventListener('mousedown', function(event) {
//         isDragging = true;

//         initX = event.clientX; // Assign value to initX
//         initY = event.clientY; // Assign value to initY

//         // Show the line
//         line.style.display = 'block';
//     });

//     // Add mousemove event listener to track mouse movement
//     document.addEventListener('mousemove', function(event) {
//         if (isDragging) {
//             var adjustedX = event.clientX - initX + parseFloat(cueball.getAttribute('cx'));
//             var adjustedY = event.clientY - initY + parseFloat(cueball.getAttribute('cy'));
//             // Update the line position to end at the adjusted mouse position
//             line.setAttribute('x2', adjustedX);
//             line.setAttribute('y2', adjustedY);
//         }
//     });

//     // Add mouseup event listener to stop dragging
//     document.addEventListener('mouseup', function() {
//         isDragging = false;

//         var finalX = event.clientX
//         var finalY = event.clientY

//         console.log(finalX)
//         console.log(finalY)
//         // Hide the line when dragging stops
//         line.style.display = 'none';
//     });
// });

document.addEventListener('DOMContentLoaded', function() {
    let lastSvgFilename = null;
    let last_svg_index = 0;
    const form = document.getElementById('playerNamesForm');

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const player1Name = document.getElementById('player1Name').value;
        const player2Name = document.getElementById('player2Name').value;

        let arr = [player1Name,  player2Name];
        const randomPlayerName = arr[Math.floor(Math.random() * arr.length)];

        console.log(randomPlayerName);
        document.getElementById('gameStatus').innerHTML = "<br> Server randomly decides that <b> "+randomPlayerName+" </b>shall play <br>\
                                                           <br> Low Ball Player :- *to be identified*    <br>\
                                                           <br> High Ball Player:- *to be identified*   <br>\
                                                            ";

        fetch('/initializeGame', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ player1Name, player2Name })
        })
        .then(response => response.json())
        .then(data => {
            if (data.tableId) {
                loadSVGContent(data.tableId);
            }
        })
        .catch(error => {
            console.error('Error initializing game:', error);
        });
    });

    function loadLastSvgAsInitialState() {
        if (lastSvgFilename) {
            const svgPath = `svgs/${last_svg_index}`;  // Construct the path to fetch the SVG
            loadSVGContent(svgPath);  // Reuse your existing function to load and display the SVG
        }
    }

    function loadSVGContent(tableId) {
        fetch(`/getSVG/${tableId}`)
        .then(response => response.text())
        .then(svgData => {
            const svgContainer = document.getElementById('svgContainer');
            svgContainer.innerHTML = svgData;

            const svgElement = svgContainer.querySelector('svg');
            if (!svgElement) {
                console.error('SVG element not found inside the container');
                return;
            }

            const cueBall = svgElement.querySelector('circle[fill="WHITE"]');
            if (cueBall) {
                bindCueBallEvents(cueBall, svgElement);
            }
        })
        .catch(error => {
            console.error('Error loading SVG:', error);
        });
    }

    function bindCueBallEvents(cueBall, svgElement) {
        let isDragging = false;
        let line = null;
        let startX, startY;

        cueBall.addEventListener('mousedown', function(event) {
            event.preventDefault();
            startX = parseFloat(cueBall.getAttribute('cx'));
            startY = parseFloat(cueBall.getAttribute('cy'));
            isDragging = true;

            line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', startX);
            line.setAttribute('y1', startY);
            line.setAttribute('stroke', 'red');
            line.setAttribute('stroke-width', '5');
            svgElement.appendChild(line);
        });

        document.addEventListener('mousemove', function(event) {
            if (!isDragging || !line) return;

            const rect = svgElement.getBoundingClientRect();
            const scaleX = svgElement.viewBox.baseVal.width / rect.width;
            const scaleY = svgElement.viewBox.baseVal.height / rect.height;

            const mouseX = (event.clientX - rect.left) * scaleX + svgElement.viewBox.baseVal.x;
            const mouseY = (event.clientY - rect.top) * scaleY + svgElement.viewBox.baseVal.y;

            line.setAttribute('x2', mouseX);
            line.setAttribute('y2', mouseY);
        });

        document.addEventListener('mouseup', function(event) {
            if (line) {
                const { xvel, yvel } = calculateInitialVelocity(event, cueBall, svgElement);
                console.log("Calculated velocities:", { xvel, yvel }); // Log velocities for debugging

                // Send the calculated data to the server
                sendShotData(xvel, yvel).then(data => {
                    // Once shot data is processed, animate SVGs if filenames are received
                    if (data.svgFilenames) {
                        animateSVGs(data.svgFilenames);
                    }
                });

                line.remove(); // Remove the line
                line = null;  // Reset the line variable
            }
            isDragging = false; // Reset dragging state
            loadLastSvgAsInitialState();

        });
    }

    function calculateInitialVelocity(event, cueBall, svgElement) {
        const rect = svgElement.getBoundingClientRect();
        const scaleX = svgElement.viewBox.baseVal.width / rect.width;
        const scaleY = svgElement.viewBox.baseVal.height / rect.height;

        const mouseX = (event.clientX - rect.left) * scaleX + svgElement.viewBox.baseVal.x;
        const mouseY = (event.clientY - rect.top) * scaleY + svgElement.viewBox.baseVal.y;

        const dx = mouseX - parseFloat(cueBall.getAttribute('cx'));
        const dy = mouseY - parseFloat(cueBall.getAttribute('cy'));

        const scaleFactor = 2.5; // Adjust based on your setup

        const xvel = dx * scaleFactor;
        const yvel = dy * scaleFactor;

        return { xvel, yvel };
    }

    function sendShotData(xvel, yvel) {
        const playerName = document.getElementById('player1Name').value;
        const postData = {
            gameName: 'Game Name',
            playerName: playerName,
            xvel: xvel,
            yvel: yvel
        };
    
        return fetch('/shoot', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(postData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.svgFilenames) {
                animateSVGs(data.svgFilenames);
            }
            if (data.lastSvgFilename) {
                lastSvgFilename = data.lastSvgFilename;
                last_svg_index = data.lastIndex;  // Store the last SVG filename
            }
        })
        .catch(error => {
            console.error('Error processing shot:', error);
        });
    }

    function animateSVGs(svgFilenames) {
        let currentSVGIndex = 0;
        let svgDataArray = [];
        let lastFrameTime = 0;
        const frameInterval = 1000 / 12; // Adjust the FPS to control the animation speed
    
        // Function to preload SVG data in parallel
        async function preloadSVGs() {
            try {
                // Create an array of fetch promises for each SVG
                const fetchPromises = svgFilenames.map((filename, index) => fetch(`/getSVG/${index}`).then(response => response.text()));
    
                // Wait for all fetch promises to resolve
                svgDataArray = await Promise.all(fetchPromises);
    
                // Start the animation after preloading
                lastFrameTime = performance.now();
                requestAnimationFrame(displayNextSVG);
            } catch (error) {
                console.error('Error preloading SVGs:', error);
            }
        }
    
        // Function to display the next SVG at controlled intervals
        function displayNextSVG(timestamp) {
            if (currentSVGIndex >= svgDataArray.length) return; // Stop if no more SVGs
    
            // Display the next SVG only if enough time has passed since the last frame
            if (timestamp - lastFrameTime > frameInterval) {
                document.getElementById('svgContainer').innerHTML = svgDataArray[currentSVGIndex++];
                lastFrameTime = timestamp;
            }
    
            // Request the next frame
            requestAnimationFrame(displayNextSVG);
        }
    
        preloadSVGs(); // Start the preloading and animation process
    }
        
    

    function calculateBallVelocity(cueBall, svgElement) {
        let line = null;
        let startX, startY;
        startX = parseFloat(cueBall.getAttribute('cx'));
        startY = parseFloat(cueBall.getAttribute('cy'));
        const rect = svgElement.getBoundingClientRect();
        const scaleOuterX = svgElement.viewBox.baseVal.width / rect.width;
        const scaleOuterY = svgElement.viewBox.baseVal.height / rect.height;

    }

    function detectAnotherBallCollision(cueBall, svgElement) {
        let line = null;
        let startX, startY;
        startX = parseFloat(cueBall.getAttribute('cx'));
        startY = parseFloat(cueBall.getAttribute('cy'));
        const scaleOuterX = svgElement.viewBox.baseVal.width / rect.width;
        const scaleOuterY = svgElement.viewBox.baseVal.height / rect.height;
    }

    function detectHitToEdgeOfTable(cueBall, svgElement) {
        let line = null;
        let startX, startY;
        startX = parseFloat(cueBall.getAttribute('cx'));
        startY = parseFloat(cueBall.getAttribute('cy'));
        const scaleOuterX = svgElement.viewBox.baseVal.width / rect.width;
        const scaleOuterY = svgElement.viewBox.baseVal.height / rect.height;
    }

    function detectSinkToPocket(cueBall, svgElement) {
        let line = null;
        let startX, startY;
        startX = parseFloat(cueBall.getAttribute('cx'));
        startY = parseFloat(cueBall.getAttribute('cy'));
        const scaleOuterX = svgElement.viewBox.baseVal.width / rect.width;
        const scaleOuterY = svgElement.viewBox.baseVal.height / rect.height;
    }
    
    function assignPlayerAsHighOrLow(cueBall, svgElement) {
        let line = null;
        let startX, startY;
        startX = parseFloat(cueBall.getAttribute('cx'));
        startY = parseFloat(cueBall.getAttribute('cy'));
        
    }

    function calculateBallVelocity(cueBall, svgElement) {
        let line = null;
        let startX, startY;
        startX = parseFloat(cueBall.getAttribute('cx'));
        startY = parseFloat(cueBall.getAttribute('cy'));
        const rect = svgElement.getBoundingClientRect();
        const scaleOuterX = svgElement.viewBox.baseVal.width / rect.width;
        const scaleOuterY = svgElement.viewBox.baseVal.height / rect.height;

    }

    function detectAnotherBallCollision(cueBall, svgElement) {
        let line = null;
        let startX, startY;
        startX = parseFloat(cueBall.getAttribute('cx'));
        startY = parseFloat(cueBall.getAttribute('cy'));
        const scaleOuterX = svgElement.viewBox.baseVal.width / rect.width;
        const scaleOuterY = svgElement.viewBox.baseVal.height / rect.height;
    }

    function detectHitToEdgeOfTable(cueBall, svgElement) {
        let line = null;
        let startX, startY;
        startX = parseFloat(cueBall.getAttribute('cx'));
        startY = parseFloat(cueBall.getAttribute('cy'));
        const scaleOuterX = svgElement.viewBox.baseVal.width / rect.width;
        const scaleOuterY = svgElement.viewBox.baseVal.height / rect.height;
    }

    function detectSinkToPocket(cueBall, svgElement) {
        let line = null;
        let startX, startY;
        startX = parseFloat(cueBall.getAttribute('cx'));
        startY = parseFloat(cueBall.getAttribute('cy'));
        const scaleOuterX = svgElement.viewBox.baseVal.width / rect.width;
        const scaleOuterY = svgElement.viewBox.baseVal.height / rect.height;
    }
    
    function assignPlayerAsHighOrLow(cueBall, svgElement) {
        let line = null;
        let startX, startY;
        startX = parseFloat(cueBall.getAttribute('cx'));
        startY = parseFloat(cueBall.getAttribute('cy'));
        
    }
});

