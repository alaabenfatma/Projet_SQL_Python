insert into LesSpectacles(noSpec, nomSpec, prixBaseSpec) values (1, 'How to be a parisian ?', 25.0);
insert into LesSpectacles(noSpec, nomSpec, prixBaseSpec) values (2, 'Je parle toute seule', 20);

insert into LesZones(noZone, catZone, tauxZone) values (1, 'poulailler', 1);
insert into LesZones(noZone, catZone, tauxZone) values (2, 'orchestre', 1.5);
insert into LesZones(noZone, catZone, tauxZone) values (3, 'balcon', 2);

insert into LesPlaces(noPlace, noRang, noZone) values (1, 1, 1);
insert into LesPlaces(noPlace, noRang, noZone) values (2, 1, 1);
insert into LesPlaces(noPlace, noRang, noZone) values (3, 1, 1);
insert into LesPlaces(noPlace, noRang, noZone) values (4, 1, 1);
insert into LesPlaces(noPlace, noRang, noZone) values (5, 1, 1);

insert into LesPlaces(noPlace, noRang, noZone) values (1, 2, 1);
insert into LesPlaces(noPlace, noRang, noZone) values (2, 2, 1);
insert into LesPlaces(noPlace, noRang, noZone) values (3, 2, 1);
insert into LesPlaces(noPlace, noRang, noZone) values (4, 2, 1);
insert into LesPlaces(noPlace, noRang, noZone) values (5, 2, 1);

insert into LesPlaces(noPlace, noRang, noZone) values (1, 3, 2);
insert into LesPlaces(noPlace, noRang, noZone) values (2, 3, 2);
insert into LesPlaces(noPlace, noRang, noZone) values (3, 3, 2);
insert into LesPlaces(noPlace, noRang, noZone) values (4, 3, 2);
insert into LesPlaces(noPlace, noRang, noZone) values (5, 3, 2);

insert into LesPlaces(noPlace, noRang, noZone) values (1, 4, 3);
insert into LesPlaces(noPlace, noRang, noZone) values (2, 4, 3);
insert into LesPlaces(noPlace, noRang, noZone) values (3, 4, 3);
insert into LesPlaces(noPlace, noRang, noZone) values (4, 4, 3);
insert into LesPlaces(noPlace, noRang, noZone) values (5, 4, 3);

insert into LesDossiers_base(noDos) values (1);
insert into LesDossiers_base(noDos) values (2);
insert into LesDossiers_base(noDos) values (3);

insert into LesRepresentations_base(noSpec, dateRep, promoRep) values (1, '24/12/2019 17:00', 1);
insert into LesRepresentations_base(noSpec, dateRep, promoRep) values (1, '25/12/2019 20:00', 0.75);
insert into LesRepresentations_base(noSpec, dateRep, promoRep) values (1, '26/12/2019 21:00', 1);
insert into LesRepresentations_base(noSpec, dateRep, promoRep) values (2, '24/12/2019 21:00', 1);
insert into LesRepresentations_base(noSpec, dateRep, promoRep) values (2, '25/12/2019 23:00', 0.5);


insert into LesTickets(noSpec, dateRep, noPlace, noRang, dateEmTick, noDos) values (1, '24/12/2019 17:00', 1, 1, '23/12/2019 21:30:20',1);
insert into LesTickets(noSpec, dateRep, noPlace, noRang, dateEmTick, noDos) values (1, '24/12/2019 17:00', 2, 1, '23/12/2019 21:30:20',1);
insert into LesTickets(noSpec, dateRep, noPlace, noRang, dateEmTick, noDos) values (1, '24/12/2019 17:00', 3, 1, '23/12/2019 21:30:20',1);
insert into LesTickets(noSpec, dateRep, noPlace, noRang, dateEmTick, noDos) values (1, '24/12/2019 17:00', 4, 1, '23/12/2019 21:30:20',1);
insert into LesTickets(noSpec, dateRep, noPlace, noRang, dateEmTick, noDos) values (1, '24/12/2019 17:00', 5, 1, '23/12/2019 21:30:20',1);

insert into LesTickets(noSpec, dateRep, noPlace, noRang, dateEmTick, noDos) values (2, '25/12/2019 23:00', 1, 2, '20/12/2019 22:31:00',2);
insert into LesTickets(noSpec, dateRep, noPlace, noRang, dateEmTick, noDos) values (2, '25/12/2019 23:00', 2, 2, '20/12/2019 22:31:00',2);

insert into LesTickets(noSpec, dateRep, noPlace, noRang, dateEmTick, noDos) values (2, '25/12/2019 23:00', 1, 3, '20/12/2019 14:22:00',3);
insert into LesTickets(noSpec, dateRep, noPlace, noRang, dateEmTick, noDos) values (2, '25/12/2019 23:00', 2, 3, '20/12/2019 14:22:00',3);