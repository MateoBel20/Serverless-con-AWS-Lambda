const AWS = require("aws-sdk");
exports.updateTask = async (event) => {
  const dynamodb = new AWS.DynamoDB.DocumentClient();
  const { id } = event.pathParameters;
  const { done, title, description } = JSON.parse(event.body);
  await dynamodb
    .update({
      TableName: "TaskTable",
      Key: { id },
      UpdateExpression:
        "set done = :done, title = :title, description = :description",
      ExpressionAttributeValues: {
        ":done": done,
        ":title": title,
        ":description": description,
      },
      ReturnValues: "ALL_NEW",
    })
    .promise();
  return {
    status: 200,
    body: JSON.stringify({
      message: "Tarea Actualizada :D",
    }),
  };
};
