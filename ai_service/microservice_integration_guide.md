# AI Microservice Integration Guide

## 1. Overview

This document explains how to call the **Python AI Microservice** (FastAPI) from your **Spring Boot Application**.

- **Base URL**: `http://localhost:8000/api`
- **Documentation (UI)**: `http://localhost:8000/docs`

## 2. Starting the Service

Before your Spring Boot app can call it, the Python server must be running.

**Windows Command:**

```bash
cd ai_service
# Activate your python env if you have one
python -m uvicorn backend.main:app --reload --port 8000
```

---

## 3. Endpoints

### A. Analyze Food Image

- **URL**: `/analyze`
- **Method**: `POST`
- **Format**: `Multipart/form-data`
- **Input**: Key=`file`, Value=`[Image File]`
- **Output**: JSON containing detected food, nutritional info, and health score.

### B. Chat with Coach

- **URL**: `/coach/chat`
- **Method**: `POST`
- **Format**: `JSON`
- **Input**:
  ```json
  {
    "message": "Can I eat pizza effectively?",
    "history": [],
    "context_data": {}
  }
  ```
- **Output**:
  ```json
  {
    "reply": "Yes, but perform it in moderation..."
  }
  ```

---

## 4. Spring Boot Integration (Java Examples)

Add `Spring Web` dependency (`spring-boot-starter-web-flux` for WebClient or just `starter-web` for RestTemplate).

### A. Calling the Analysis Endpoint (Multipart)

```java
import org.springframework.core.io.ByteArrayResource;
import org.springframework.http.MediaType;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

public class AIServiceClient {

    private final WebClient webClient;

    public AIServiceClient(WebClient.Builder builder) {
        this.webClient = builder.baseUrl("http://localhost:8000/api").build();
    }

    // Call /analyze
    public String analyzeFoodImage(byte[] imageBytes, String filename) {
        MultipartBodyBuilder builder = new MultipartBodyBuilder();
        builder.part("file", new ByteArrayResource(imageBytes))
               .header("Content-Disposition", "form-data; name=file; filename=" + filename);

        return webClient.post()
                .uri("/analyze")
                .contentType(MediaType.MULTIPART_FORM_DATA)
                .body(BodyInserters.fromMultipartData(builder.build()))
                .retrieve()
                .bodyToMono(String.class) // Returns raw JSON string, map to DTO in production
                .block();
    }
}
```

### B. Calling the Chat Endpoint (JSON)

```java
import java.util.List;
import java.util.Map;

// DTOs
record ChatRequest(String message, List<Object> history, Object context_data) {}
record ChatResponse(String reply) {}

public String chatWithCoach(String userMessage) {
    ChatRequest request = new ChatRequest(userMessage, List.of(), null);

    return webClient.post()
            .uri("/coach/chat")
            .contentType(MediaType.APPLICATION_JSON)
            .bodyValue(request)
            .retrieve()
            .bodyToMono(ChatResponse.class)
            .map(ChatResponse::reply)
            .block();
}
```

---

## 5. Notes for Production

- **Timeout**: The Vision Model can take 5-10 seconds. Configure your `WebClient` timeout accordingly.
- **Security**: Ensure the endpoints are not exposed publicly if this service acts as an internal backend.
