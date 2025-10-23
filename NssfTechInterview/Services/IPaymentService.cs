using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace NssfTechInterview.Service
{
    public interface IPaymentService
    {
        public bool ProcessPayment(int userId, decimal amount);
    }
}
