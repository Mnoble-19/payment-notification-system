@app.post("/bank-notification")
async def process_bank_notification(notification: Dict):
    try:
        notif_text = notification.get('notification_text')
        if not notif_text:
            raise HTTPException(status_code=400, detail="Missing notification text")

        logger.info(f"Processing notification: {notif_text}")

        # Extract data
        try:
            amount = extract_amount(notif_text)
            date = extract_date(notif_text)
            description = extract_description(notif_text)
        except ValueError as e:
            logger.error(f"Parsing error: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            # Find matching customer
            cur.execute("""
                SELECT customer_id, first_name, last_name 
                FROM customers 
                WHERE customer_alias ILIKE %s
            """, (description.split()[-1],))

            customer = cur.fetchone()

            if not customer:
                logger.error(f"No customer found for description: {description}")
                raise HTTPException(status_code=404, detail="Customer not found")

            # Insert transaction
            cur.execute("""
                INSERT INTO transactions 
                (customer_id, amount, transaction_date, description, raw_notification, status)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING transaction_id
            """, (
                customer['customer_id'],
                amount,
                date,
                description,
                notif_text,
                'completed'
            ))

            transaction_id = cur.fetchone()['transaction_id']
            conn.commit()

            # Send confirmation
            transaction_details = {
                "transaction_id": str(transaction_id),
                "amount": amount,
                "date": date.isoformat(),
                "description": description
            }

            await send_confirmation(customer['customer_id'], transaction_details)

            return {
                "status": "success",
                "transaction_id": transaction_id,
                "customer_id": customer['customer_id']
            }

        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {str(e)}")
            raise HTTPException(status_code=500, detail="Database error")
        finally:
            cur.close()
            conn.close()

    except Exception as e:
        logger.error(f"Processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Processing error")


@app.get("/transactions/{customer_id}")
async def get_customer_transactions(customer_id: str):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT transaction_id, amount, transaction_date, description, status
            FROM transactions
            WHERE customer_id = %s
            ORDER BY transaction_date DESC
        """, (customer_id,))

        transactions = cur.fetchall()
        return {"transactions": [dict(t) for t in transactions]}

    finally:
        cur.close()
        conn.close()