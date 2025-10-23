The ticket line is a dotnet core project that targets .NET 8.0 and uses C# 12.0 as the programming language version.

To set up a .NET 8.0 project with C# 12.0, ensure your project file (.csproj) includes the following configurations:

The implementation makes use of a minimal API approach to create a simple web application that responds with "Hello, World!" when accessed via the root URL.

With 4 endpoints;
    1 - POST /reserve - This reserves a ticket.
    2 - GET /confirm - This confirms a paritcular reservation.
    3 - GET /purchase - Gets a particular purchase.
    4 - GET /purchases - Gets all current purchases.

The application uses an in-memory list to store ticket reservations and purchases for demonstration purposes.

As well as a simulated background that processes completed reservations into purchases.Sending out would be emails.