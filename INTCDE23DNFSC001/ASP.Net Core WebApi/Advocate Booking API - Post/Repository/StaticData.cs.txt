using PostWebApi.Interface;
using PostWebApi.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace PostWebApi.Repository
{
    public class StaticData
    {
        public static List<Client> lsClients = new List<Client>
        {
            new Client{CaseId=10001, CaseDescription="Damage to property", CaseDate="15/10/2022", Name="RajKumar", PhoneNumber="1234567890", EmailId="user1@test.com" },
            new Client{CaseId=10002, CaseDescription="Landlord and tenant disputes", CaseDate="25/10/2022", Name="AravindSwamy", PhoneNumber="2334567890", EmailId="user2@test.com" },
            new Client{CaseId=10003, CaseDescription="Back rent", CaseDate="30/10/2022", Name="RahulDravid", PhoneNumber="3234567890", EmailId="user3@test.com" },
            new Client{CaseId=10004, CaseDescription="Damage to property", CaseDate="15/10/2022", Name="PreethiSingh", PhoneNumber="4123567890", EmailId="user4@test.com" },
            new Client{CaseId=10005, CaseDescription="Unpaid personal loans", CaseDate="15/10/2022", Name="LaxmiDevi", PhoneNumber="2345167890", EmailId="user5@test.com" },
        };

    }
}
