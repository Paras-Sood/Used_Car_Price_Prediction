document.addEventListener('DOMContentLoaded',()=>{
    addgraph('year')
    document.querySelector('#column1_selector').onchange = function(){addgraph(this.value)}
    document.querySelector('form').onsubmit = function(){
        document.querySelector('#output').style.display='block'
        document.querySelector('#output h2').innerHTML="Loading..."
        fetch('/predict',{
            method:'POST',
            credentials: "include",
            body: JSON.stringify({
                "brand":[document.querySelector('#brand').value],
                "year":[parseInt(document.querySelector('#year').value)],
                "transmission":[document.querySelector('#transmission').value],
                "mileage":[parseInt(document.querySelector('#mileage').value)],
                "fuelType":[document.querySelector('#fuel_type').value],
                "tax":[parseInt(document.querySelector('#tax').value)],
                "mpg":[parseInt(document.querySelector('#mpg').value)],
                "engineSize":[parseInt(document.querySelector('#eng_size').value)],
            }),
            cache: "no-cache",
            headers: new Headers({
            "content-type": "application/json"
            })
        })
        .then(response=>response.json())
        .then(response=>{
            document.querySelector('#output h2').innerHTML=`The predicted price is $ ${response.Price}`
        });
        return false
    }
})
function addgraph(column){
    fetch(`/data?column=${column}`)
    .then(response=>response.json())
    .then(response=>{
        let xValues=[]
        let yValues=[]
        response.forEach(ele => {
            xValues.push(ele[0])
            yValues.push(ele[1])
        });
        document.querySelector('#graph_div').innerHTML=""
        let canvas=document.createElement('canvas')
        canvas.id="graph"
        document.querySelector('#graph_div').append(canvas)
        type_graph="line"
        if(column==="brand" || column==="transmission" || column==="fuelType")    type_graph="bar"
        new Chart("graph", {
            type: type_graph,
            data: {
                labels: xValues,
                datasets: [{
                    fill: false,
                    lineTension: 0.25,
                    backgroundColor: "rgba(0,0,255,1.0)",
                    borderColor: "red",
                    data: yValues
                }]
            },
            options: {
                plugins:{   
                    legend: {
                        display: false
                        },
                    title: {
                        display: true,
                        text: `Average Price of car for different ${column[0].toUpperCase()+column.slice(1)}`
                    },
                },
                scales: {
                    xAxis: {
                        ticks: {
                            maxTicksLimit: 10,
                        },
                    },
                }
            }
        })
    })
}