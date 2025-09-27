filter_schema_example = {
  "name": "New Filter",
  "logical_operator": "OR",
  "conditions": [
    {
      "logical_operator": "AND",
      "conditions": [
        {"field": "price", "operator": ">", "value": 100},
        {"field": "stock", "operator": ">=", "value": 10}
      ]
    },
    {
      "logical_operator": "AND",
      "conditions": [
        {"field": "features", "operator": "include", "value": "waterproof"},
        {"field": "discount", "operator": "<=", "value": 20}
      ]
    }
  ]
}
