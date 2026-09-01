import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';

export async function GET(context) {
  const lessons = (await getCollection('lessons')).filter(
    (lesson) => !lesson.data.draft,
  );

  return rss({
    title: 'The Unexpected Professor',
    description:
      "Leçons, vidéos et laboratoires interactifs sur l'électronique de puissance et la conversion d'énergie.",
    site: context.site,
    items: lessons
      .filter((lesson) => lesson.data.published_at)
      .sort((a, b) => b.data.published_at - a.data.published_at)
      .map((lesson) => ({
        title: lesson.data.title,
        description: lesson.data.summary,
        pubDate: lesson.data.published_at,
        link: `/lessons/${lesson.id}`,
      })),
    customData: '<language>fr-fr</language>',
  });
}
