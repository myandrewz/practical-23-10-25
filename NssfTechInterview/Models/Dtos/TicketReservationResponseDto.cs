using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using static NssfTechInterview.Utils.Enums;

namespace NssfTechInterview.Models.Dtos
{
    public class TicketReservationResponseDto
    {
        public string ResponseCode  { get; set; }

        public ReservationStatus Status { get; set; } = ReservationStatus.Pending;
    }
}
