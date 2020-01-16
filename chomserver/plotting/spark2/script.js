function generateRandomData(seriesCount, datesCount) {
  return d3.range(seriesCount).map(function (d) {
    return {
      name: '#' + d,
      values: d3.range(datesCount).map(function (d) {
        return {
          label: d,
          value: Math.random(d)
        };
      })
    };
  });
}

var sparklinesConfig = {
  height: 20,
  width: 180
};

// Sparklines configuration
var sparklines = d3.toucan.sparklines()
  .height(sparklinesConfig.height)
  .width(sparklinesConfig.width)
  .dateSelector('label')
  .forceLexicalOrder(false)
  .valueSelector('value')
  .valueFormat('.2p')
  .unit('');

function createOrUpdateSparklines() {
  var exampleElement = d3.selectAll('#example')

  // Adding some sample parents elements
  var categoriesSelection = exampleElement.selectAll('.category')
    .data(generateRandomData(10, 30), function(cat) {
      return cat.name;
    });

  var newCategories = categoriesSelection
    .enter()
    .append('div')
    .classed('category', true);

  newCategories
    .append('span')
    .classed('category__label', true)

  categoriesSelection.select('.category__label')
    .text(function (d) {
      return d.name;
    });

  // Creating blocks that will contain sparklines
  var newSparklinesSelection = newCategories
    .append('svg')
    .classed('sparkline', true)
    .attr('height', sparklinesConfig.height)
    .attr('width', sparklinesConfig.width)

  // Binding data to them
  var sparklinesSelection = categoriesSelection.select('.sparkline')
    .datum(function (d) {
      return d.values;
    });

  newCategories
    .append('span')
    .classed('category__value', true)

  var valueFormatter = d3.format('.2p');
  categoriesSelection.select('.category__value')
    .text(function (d) {
      return valueFormatter(d.values[d.values.length - 1].value);
    });

  // Do the magic!
  sparklinesSelection
    .call(sparklines);
}

createOrUpdateSparklines();