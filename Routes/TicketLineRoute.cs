using Microsoft.EntityFrameworkCore;
using questionthree.Database;
using questionthree.Models;
using questionthree.Services;

namespace questionthree.Routes
{
    public static class TicketLineRoute
    {

        /// <summary>
        /// Configures API endpoints for ticket reservation, confirmation, and purchase retrieval in the application.
        /// </summary>
        /// <remarks>This method registers endpoints for reserving tickets, confirming reservations, and
        /// retrieving purchase information. It should be called during application startup to enable these routes. The
        /// confirmation endpoint also triggers background notification processing for completed purchases.</remarks>
        /// <param name="app">The <see cref="WebApplication"/> instance to which the ticket-related routes will be mapped.</param>
        public static void MapTicketLineRoutes(this WebApplication app)
        {

            app.MapPost("api/v1/reserve", async (Reservation reservation, IReservationService reservationService) =>
            {
                await reservationService.AddReservation(reservation);
                return Results.Ok(reservation);
            });

            app.MapPost("api/v1/confirm/{reservationId}", async (IPurchaseService purchaseService, INotificationService notificationService, int reservationId) =>
            {
                
                var (added, purchase) = await purchaseService.AddPurchase(reservationId);

                if (!added)
                {
                    return Results.BadRequest("Could not confirm your reservation");
                }


                // Simulated background worker
                // In real-world, this would be it's own application
                // proper background job processor like Hangfire, Quartz.NET, or a message queue
                // to be picked up by a separate notification service

                //it's implemented this way because threads started in ASP.NET Core apps
                //can not share a db context instance with the main thread
                //so we create a new scope to get a new instance of the db context
                _ = Task.Run(async () =>
                {
                    while (true)
                    {
                        //find the scope
                        using var scope = app.Services.CreateScope();

                        //ensure to get a new db context instance from the scope
                        var db = scope.ServiceProvider.GetRequiredService<AppDbContext>();

                        var pending = await db.OutboxEvents
                            .Where(e => !e.Processed)
                            .ToListAsync();

                        foreach (var evt in pending)
                        {
                            // Simulate sending notification
                            await notificationService.SendPurchaseNotification(evt.Payload);

                            // Mark as processed
                            evt.Processed = true;
                        }

                        await db.SaveChangesAsync();
                        await Task.Delay(1000);
                    }
                });


                return Results.Ok(purchase);
            });


            app.MapGet("api/v1/purchase/{purchaseId}", async (IPurchaseService purchaseService,int purchaseId) =>
                    await purchaseService.GetPurchaseById(purchaseId));


            app.MapGet("api/v1/purchases", async (IPurchaseService purchaseService) =>
                   await purchaseService.GetPurchases());
          
        }

        
    }
}
