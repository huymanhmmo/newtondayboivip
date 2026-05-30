import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const coursesCollection = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: "./src/content/courses" }),
  schema: z.object({
    title: z.string(),
    price_group_1: z.string(),
    price_group_1_desc: z.string(),
    price_group_2: z.string().optional(),
    price_group_2_desc: z.string().optional(),
    image: z.string().optional(),
    order: z.number()
  })
});

const faqsCollection = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: "./src/content/faqs" }),
  schema: z.object({
    question: z.string(),
    order: z.number()
  })
});

const testimonialsCollection = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: "./src/content/testimonials" }),
  schema: z.object({
    name: z.string(),
    role: z.string(),
    avatar: z.string().optional(),
    stars: z.number().default(5),
    order: z.number()
  })
});

const blogCollection = defineCollection({
  loader: glob({ pattern: '**/[^_]*.md', base: "./src/content/blog" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.date(),
    image: z.string().optional(),
    tags: z.array(z.string()).default([])
  })
});

export const collections = {
  courses: coursesCollection,
  faqs: faqsCollection,
  testimonials: testimonialsCollection,
  blog: blogCollection
};
