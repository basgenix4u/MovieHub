import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://placeholder.supabase.co';
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'placeholder-key';

// We use a try-catch or conditional to ensure the app doesn't crash during Vercel's build phase
export const supabase = createClient(supabaseUrl, supabaseAnonKey);
