
using Microsoft.EntityFrameworkCore;
using questionthree.Database;
using questionthree.Routes;
using questionthree.Services;
using System;
using System.Reflection;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddDbContext<AppDbContext>(opt =>
    opt.UseInMemoryDatabase("inmemoryticketlineDB"));
builder.Services.AddEndpointsApiExplorer();

//map services
builder.Services.AddScoped<IReservationService, ReservationService>();
builder.Services.AddScoped<IPurchaseService, PurchaseService>();
builder.Services.AddScoped<INotificationService, NotificationService>();

builder.Services.AddSwaggerGen(options =>
{
    var xmlFile = $"{Assembly.GetExecutingAssembly().GetName().Name}.xml";
    var xmlPath = Path.Combine(AppContext.BaseDirectory, xmlFile);
    options.IncludeXmlComments(xmlPath);
});

var app = builder.Build();
app.UseSwagger();
app.UseSwaggerUI();
app.UseHttpsRedirection();

//add routes
app.MapTicketLineRoutes();


app.Run();