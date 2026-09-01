import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Lesson front-matter contract (hub section 5.3). The schema is intentionally
// close to that draft; fields are tightened as the lesson template is built
// out in later commits. `youtube_id` and `lab_url` stay nullable so a lesson
// can be written and previewed before its video or lab exists.
const lessons = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: './src/content/lessons' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    language: z.enum(['fr', 'en']).default('fr'),
    level: z
      .enum(['secondary', 'undergraduate', 'graduate', 'professional'])
      .default('undergraduate'),
    duration_minutes: z.number().int().positive().optional(),
    topics: z.array(z.string()).default([]),
    course_sequence: z.string().optional(),
    sequence_index: z.number().int().nonnegative().optional(),
    objectives: z.array(z.string()).default([]),
    prerequisites: z.array(z.string()).default([]),
    sources: z
      .array(z.object({ label: z.string(), href: z.string().url() }))
      .default([]),
    youtube_id: z.string().nullable().default(null),
    lab_url: z.string().url().nullable().default(null),
    published_at: z.coerce.date().nullable().default(null),
    updated_at: z.coerce.date().nullable().default(null),
    authors: z.array(z.string()).default(['The Unexpected Professor']),
    licence: z.string().default('CC-BY-SA-4.0'),
    draft: z.boolean().default(true),
    // Private cross-reference to the IUT course; never shown in public
    // navigation (hub section 5.1).
    course_ref: z.string().optional(),
  }),
});

export const collections = { lessons };
