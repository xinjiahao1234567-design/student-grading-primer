# Edge Case

## Identified edge case
An edge case in the spec is what `/stats` should return when there are no valid student marks available.

This can happen if:
- there are no students in the database, or
- student records exist but none of them have a mark recorded.

## How I handled it
I chose to make the `/stats` endpoint return a valid success response instead of treating this as an error.

In this situation, the backend returns:

```json
{
  "count": 0,
  "average": null,
  "min": null,
  "max": null
}
```

## Why this is a reasonable choice
This keeps the API predictable and avoids failing when the database is empty.
It also clearly tells the frontend that there is currently no mark data to summarise, while still returning a consistent response shape.
