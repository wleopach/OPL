fetch('Data/graph_data.json')
    .then(response => response.json())
    .then(data => {
        const nodes = data.nodes.map(node => ({
            id: node.id,
            color: node.color,
            city: node.city
        }));
        console.log(nodes);

        const links = data.links.map(link => ({
            source: link.source,
            target: link.target
        }));
        console.log(links);

        const Graph = ForceGraph3D()
            .nodeLabel('city')
            .nodeColor('color')
            .linkSource('source')
            .linkTarget('target')
            .width(window.innerWidth)
            .height(window.innerHeight)
            .graphData({nodes, links});

        Graph(document.getElementById('graph-container2'));
    })
    .catch(error => console.error('Error fetching data:', error));