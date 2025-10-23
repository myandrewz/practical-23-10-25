package dev.brightkan.ticket_line.service;

import dev.brightkan.ticket_line.dto.EventRequest;
import dev.brightkan.ticket_line.dto.EventResponse;
import dev.brightkan.ticket_line.exception.EventNotFoundException;
import dev.brightkan.ticket_line.model.entity.Event;
import dev.brightkan.ticket_line.repository.EventRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class EventService {

    private final EventRepository eventRepository;

    @Transactional
    public EventResponse createEvent(EventRequest request) {
        log.info("Creating new event: {}", request.getName());

        Event event = Event.builder()
                .name(request.getName())
                .description(request.getDescription())
                .eventDate(request.getEventDate())
                .venue(request.getVenue())
                .totalTickets(request.getTotalTickets())
                .availableTickets(request.getTotalTickets()) // Initially all tickets are available
                .ticketPrice(request.getTicketPrice())
                .build();

        Event savedEvent = eventRepository.save(event);

        log.info("Event created successfully: {} (ID: {})", savedEvent.getName(), savedEvent.getId());

        return toEventResponse(savedEvent);
    }

    @Transactional
    public EventResponse updateEvent(Long eventId, EventRequest request) {
        log.info("Updating event: {}", eventId);

        Event event = eventRepository.findById(eventId)
                .orElseThrow(() -> new EventNotFoundException(eventId));

        // Calculate the difference in total tickets
        int ticketDifference = request.getTotalTickets() - event.getTotalTickets();
        int newAvailableTickets = event.getAvailableTickets() + ticketDifference;

        // Ensure available tickets don't go negative
        if (newAvailableTickets < 0) {
            newAvailableTickets = 0;
        }

        event.setName(request.getName());
        event.setDescription(request.getDescription());
        event.setEventDate(request.getEventDate());
        event.setVenue(request.getVenue());
        event.setTotalTickets(request.getTotalTickets());
        event.setAvailableTickets(newAvailableTickets);
        event.setTicketPrice(request.getTicketPrice());

        Event updatedEvent = eventRepository.save(event);

        log.info("Event updated successfully: {}", eventId);

        return toEventResponse(updatedEvent);
    }

    @Transactional(readOnly = true)
    public EventResponse getEventById(Long eventId) {
        Event event = eventRepository.findById(eventId)
                .orElseThrow(() -> new EventNotFoundException(eventId));

        return toEventResponse(event);
    }

    @Transactional(readOnly = true)
    public List<EventResponse> getAllEvents() {
        List<Event> events = eventRepository.findAll();
        return events.stream()
                .map(this::toEventResponse)
                .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public List<EventResponse> getUpcomingEvents() {
        LocalDateTime now = LocalDateTime.now();
        List<Event> events = eventRepository.findByEventDateAfter(now);
        return events.stream()
                .map(this::toEventResponse)
                .collect(Collectors.toList());
    }

    @Transactional(readOnly = true)
    public List<EventResponse> getAvailableEvents() {
        LocalDateTime now = LocalDateTime.now();
        List<Event> events = eventRepository.findUpcomingEventsWithAvailableTickets(now);
        return events.stream()
                .map(this::toEventResponse)
                .collect(Collectors.toList());
    }

    @Transactional
    public void deleteEvent(Long eventId) {
        log.info("Deleting event: {}", eventId);

        Event event = eventRepository.findById(eventId)
                .orElseThrow(() -> new EventNotFoundException(eventId));

        eventRepository.delete(event);

        log.info("Event deleted successfully: {}", eventId);
    }

    @Transactional(readOnly = true)
    public Event getEventEntityById(Long eventId) {
        return eventRepository.findById(eventId)
                .orElseThrow(() -> new EventNotFoundException(eventId));
    }

    private EventResponse toEventResponse(Event event) {
        return EventResponse.builder()
                .id(event.getId())
                .name(event.getName())
                .description(event.getDescription())
                .eventDate(event.getEventDate())
                .venue(event.getVenue())
                .totalTickets(event.getTotalTickets())
                .availableTickets(event.getAvailableTickets())
                .ticketPrice(event.getTicketPrice())
                .soldOut(event.getAvailableTickets() == 0)
                .createdAt(event.getCreatedAt())
                .updatedAt(event.getUpdatedAt())
                .build();
    }
}
