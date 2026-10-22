import { createClient } from '@supabase/supabase-js'

export const supabase = createClient(
  'https://golnhrngkwbwzfltntjo.supabase.co',
  'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdvbG5ocm5na3did3pmbHRudGpvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTI1MDUyNzksImV4cCI6MjEwODA4MTI3OX0.4gJOiWDsXWCp3CRb0NZnSdK2BtMNJqXxmrxDMIPYVNw'
)