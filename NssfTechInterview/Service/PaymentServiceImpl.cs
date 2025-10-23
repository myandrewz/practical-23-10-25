using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NssfTechInterview.Service
{
    public class PaymentServiceImpl : IPaymentService
    {
        public bool ProcessPayment(int userId, decimal amount)
        {
            try
            {

                // Mock payment processing
                Console.WriteLine($"Processing payment for user {userId}, amount {amount:C}");
                return true; // Always success
            }
            catch (Exception ex)
            {
                //log error
            }
            return false;
        }
    }
}
