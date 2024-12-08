const AWS = require("aws-sdk");
exports.getTask = async (event) => {
  const dynamodb = new AWS.DynamoDB.DocumentClient();
  const result = await dynamodb
    .scan({
      TableName: "TaskTable",
    })
    .promise();
  const task = result.Items;
  return {
    status: 200,
    body: task,
  };
};















